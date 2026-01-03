function keyboardViz() {
    return {
        platform: new URLSearchParams(window.location.search).get("platform") || "yabai",
        keybinds: [],
        loading: true,
        hoverInfo: { title: "Hover a key", desc: "Hover one of the highlighted keys to see the keybinding" },
        highlightedKeys: new Set(),
        
        keyboardLayout: [
            [{code:"esc",label:"Esc"},{code:"f1",label:"F1"},{code:"f2",label:"F2"},{code:"f3",label:"F3"},{code:"f4",label:"F4"},{code:"f5",label:"F5"},{code:"f6",label:"F6"},{code:"f7",label:"F7"},{code:"f8",label:"F8"},{code:"f9",label:"F9"},{code:"f10",label:"F10"},{code:"f11",label:"F11"},{code:"f12",label:"F12"},{code:"del",label:"Del"}],
            [{code:"backtick",label:"`"},{code:"1",label:"1"},{code:"2",label:"2"},{code:"3",label:"3"},{code:"4",label:"4"},{code:"5",label:"5"},{code:"6",label:"6"},{code:"7",label:"7"},{code:"8",label:"8"},{code:"9",label:"9"},{code:"0",label:"0"},{code:"minus",label:"-"},{code:"equals",label:"="},{code:"backspace",label:"Bksp",width:"w-2"}],
            [{code:"tab",label:"Tab",width:"w-1"},{code:"q",label:"Q"},{code:"w",label:"W"},{code:"e",label:"E"},{code:"r",label:"R"},{code:"t",label:"T"},{code:"y",label:"Y"},{code:"u",label:"U"},{code:"i",label:"I"},{code:"o",label:"O"},{code:"p",label:"P"},{code:"[",label:"["},{code:"]",label:"]"},{code:"\\",label:"\\"}],
            [{code:"caps",label:"Caps",width:"w-2"},{code:"a",label:"A"},{code:"s",label:"S"},{code:"d",label:"D"},{code:"f",label:"F"},{code:"g",label:"G"},{code:"h",label:"H"},{code:"j",label:"J"},{code:"k",label:"K"},{code:"l",label:"L"},{code:";",label:";"},{code:"quote",label:"\""},{code:"enter",label:"Enter",width:"w-2"}],
            [{code:"shift",label:"Shift",width:"w-3",modifier:true},{code:"z",label:"Z"},{code:"x",label:"X"},{code:"c",label:"C"},{code:"v",label:"V"},{code:"b",label:"B"},{code:"n",label:"N"},{code:"m",label:"M"},{code:",",label:","},{code:".",label:"."},{code:"/",label:"/"},{code:"shift-r",label:"Shift",width:"w-3",modifier:true}],
            [{code:"fn",label:"fn",width:"w-1"},{code:"ctrl",label:"Ctrl",width:"w-1",modifier:true},{code:"opt",label:"Opt",width:"w-1",modifier:true},{code:"cmd",label:"Cmd",width:"w-1",modifier:true},{code:"space",label:"",width:"space"},{code:"cmd-r",label:"Cmd",width:"w-1",modifier:true},{code:"opt-r",label:"Opt",width:"w-1",modifier:true}],
            [{code:"left",label:"\u2190"},{code:"up",label:"\u2191"},{code:"down",label:"\u2193"},{code:"right",label:"\u2192"}]
        ],
        
        async init() {
            await this.fetchKeybinds();
        },
        
        async switchPlatform(p) {
            this.platform = p;
            history.pushState({}, "", "?platform=" + p);
            await this.fetchKeybinds();
        },
        
        async fetchKeybinds() {
            this.loading = true;
            try {
                const resp = await fetch("/api/keybinds/" + this.platform);
                if (resp.ok) this.keybinds = await resp.json();
            } catch (e) { console.error(e); }
            this.loading = false;
        },
        
        get groupedKeybinds() {
            const groups = {};
            this.keybinds.forEach(kb => {
                if (!groups[kb.category]) groups[kb.category] = [];
                groups[kb.category].push(kb);
            });
            return groups;
        },
        
        get activeKeys() {
            const keys = new Set();
            this.keybinds.forEach(kb => {
                keys.add(kb.key.toLowerCase());
                kb.modifiers.forEach(m => keys.add(m.toLowerCase()));
            });
            return keys;
        },
        
        getKeyClasses(key) {
            const classes = [key.width || ""];
            if (key.modifier) classes.push("modifier");
            else if (this.highlightedKeys.has(key.code) || this.highlightedKeys.has(key.code.replace("-r", ""))) {
                classes.push("active");
            } else if (this.activeKeys.has(key.code) || this.activeKeys.has(key.code.replace("-r", ""))) {
                classes.push("active");
            }
            return classes.join(" ");
        },
        
        onKeyHover(key) {
            const code = key.code.replace("-r", "");
            const matching = this.keybinds.filter(kb => 
                kb.key.toLowerCase() === code || kb.modifiers.includes(code)
            );
            if (matching.length > 0) {
                this.hoverInfo = {
                    title: matching.map(kb => this.formatKeybind(kb)).join(", "),
                    desc: matching.map(kb => kb.action).join(" | ")
                };
                this.highlightedKeys = new Set();
                matching.forEach(kb => {
                    this.highlightedKeys.add(kb.key.toLowerCase());
                    kb.modifiers.forEach(m => this.highlightedKeys.add(m));
                });
            }
        },
        
        onKeyLeave() {
            this.hoverInfo = { title: "Hover a key", desc: "Hover one of the highlighted keys to see the keybinding" };
            this.highlightedKeys = new Set();
        },
        
        highlightKeybind(kb) {
            this.highlightedKeys = new Set([kb.key.toLowerCase(), ...kb.modifiers]);
            this.hoverInfo = { title: this.formatKeybind(kb), desc: kb.action };
        },
        
        clearHighlight() {
            this.highlightedKeys = new Set();
            this.hoverInfo = { title: "Hover a key", desc: "Hover one of the highlighted keys to see the keybinding" };
        },
        
        formatKeybind(kb) {
            const mods = kb.modifiers.map(m => m.charAt(0).toUpperCase() + m.slice(1)).join(" + ");
            const key = kb.key.toUpperCase();
            return mods ? mods + " + " + key : key;
        }
    };
}
