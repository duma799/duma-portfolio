// Terminal typing animation
const terminalOutput = document.getElementById('terminal-output');
const inputLine = document.getElementById('input-line');
const terminalInput = document.getElementById('terminal-input');

const commands = [
    'neofetch',
    'cat ~/.config/hyprland/hyprland.conf | head -5',
    'skhd --version',
    'yabai --version',
    'echo "Welcome to my portfolio!"'
];

let currentCommandIndex = 0;
let isTyping = false;

function getRandomDelay() {
    return Math.floor(Math.random() * 40) + 20;
}

function createTerminalLine() {
    const line = document.createElement('div');
    line.className = 'terminal-line';

    const prompt = document.createElement('span');
    prompt.className = 'prompt';
    prompt.textContent = '$';

    const text = document.createElement('span');
    text.className = 'terminal-text';

    line.appendChild(prompt);
    line.appendChild(text);
    terminalOutput.appendChild(line);

    return text;
}

function typeCharacter(element, text, index, callback) {
    if (index < text.length) {
        element.textContent += text[index];
        setTimeout(() => {
            typeCharacter(element, text, index + 1, callback);
        }, getRandomDelay());
    } else {
        setTimeout(callback, 200);
    }
}

function typeNextCommand() {
    if (currentCommandIndex < commands.length) {
        isTyping = true;
        const textElement = createTerminalLine();
        const command = commands[currentCommandIndex];

        typeCharacter(textElement, command, 0, () => {
            currentCommandIndex++;
            typeNextCommand();
        });
    } else {
        isTyping = false;
        setTimeout(() => {
            if (inputLine && terminalInput) {
                inputLine.style.display = 'flex';
                terminalInput.focus();
            }
        }, 300);
    }
}

if (terminalInput) {
    terminalInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const command = terminalInput.value.trim();

            if (command) {
                const line = document.createElement('div');
                line.className = 'terminal-line';

                const prompt = document.createElement('span');
                prompt.className = 'prompt';
                prompt.textContent = '$';

                const text = document.createElement('span');
                text.className = 'terminal-text';
                text.textContent = command;

                line.appendChild(prompt);
                line.appendChild(text);
                terminalOutput.appendChild(line);

                const response = document.createElement('div');
                response.style.marginBottom = '0.5rem';
                response.style.color = '#808080';
                response.style.fontStyle = 'italic';

                const lowerCommand = command.toLowerCase();
                if (lowerCommand.includes('help')) {
                    response.textContent = 'Available commands: help, clear, about, dotfiles';
                } else if (lowerCommand === 'clear') {
                    terminalOutput.innerHTML = '';
                } else if (lowerCommand.includes('about')) {
                    response.textContent = 'Duma - Linux & macOS dotfiles enthusiast';
                } else if (lowerCommand.includes('dotfiles')) {
                    response.textContent = 'Check out /dotfiles for my Hyprland and Yabai configs!';
                } else {
                    response.textContent = `bash: ${command}: command not found`;
                }

                if (lowerCommand !== 'clear') {
                    terminalOutput.appendChild(response);
                }
            }

            terminalInput.value = '';

            if (terminalOutput.parentElement) {
                terminalOutput.parentElement.scrollTop = terminalOutput.parentElement.scrollHeight;
            }
        }
    });
}

const terminalBody = document.querySelector('.terminal-body');
if (terminalBody && terminalInput) {
    terminalBody.addEventListener('click', () => {
        if (!isTyping) {
            terminalInput.focus();
        }
    });
}

// Initialize terminal animation on page load
window.addEventListener('load', () => {
    setTimeout(() => {
        if (terminalOutput) {
            typeNextCommand();
        }
    }, 300);
});

// Scroll animations
const observerOptions = {
    root: null,
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.scroll-animate');
    animateElements.forEach(el => observer.observe(el));
});
