
// DOM Elements
const computerGrid = document.getElementById('computerGrid');
const searchInput = document.getElementById('searchInput');
const addComputerBtn = document.getElementById('addComputer');
const addComputerModal = document.getElementById('addComputerModal');
const addComputerForm = document.getElementById('addComputerForm');
const cancelAddBtn = document.getElementById('cancelAdd');

// State
let computers = [
  {
    id: "1",
    name: "Development PC",
    macAddress: "00:1B:44:11:3A:B7",
    status: "active",
    processingTime: "2h 15m",
  },
  {
    id: "2",
    name: "Testing Station",
    macAddress: "00:1B:44:11:3A:B8",
    status: "pending",
  },
  {
    id: "3",
    name: "Production Server",
    macAddress: "00:1B:44:11:3A:B9",
    status: "disconnected",
  }
];

// Event Listeners
addComputerBtn.addEventListener('click', () => {
  addComputerModal.style.display = 'block';
});

cancelAddBtn.addEventListener('click', () => {
  addComputerModal.style.display = 'none';
});

addComputerForm.addEventListener('submit', (e) => {
  e.preventDefault();
  
  const name = document.getElementById('computerName').value;
  const macAddress = document.getElementById('macAddress').value;
  
  const newComputer = {
    id: Math.random().toString(36).substr(2, 9),
    name,
    macAddress,
    status: "disconnected"
  };
  
  computers.push(newComputer);
  renderComputers(computers);
  addComputerModal.style.display = 'none';
  addComputerForm.reset();
});

searchInput.addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  const filteredComputers = computers.filter(computer => 
    computer.name.toLowerCase().includes(searchTerm) ||
    computer.macAddress.toLowerCase().includes(searchTerm)
  );
  renderComputers(filteredComputers);
});

// Render Functions
function renderComputers(computersToRender) {
  computerGrid.innerHTML = '';
  
  computersToRender.forEach(computer => {
    const card = document.createElement('div');
    card.className = 'computer-card';
    
    const statusColor = {
      active: 'var(--neon-green)',
      pending: 'var(--neon-purple)',
      disconnected: 'var(--neon-red)'
    }[computer.status];
    
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="color: ${statusColor}">${computer.name}</h3>
        <span class="status-dot" style="background-color: ${statusColor}; box-shadow: 0 0 10px ${statusColor}"></span>
      </div>
      <p style="color: #888; margin-bottom: 1rem;">MAC: ${computer.macAddress}</p>
      ${computer.processingTime ? `<p>Processing time: ${computer.processingTime}</p>` : ''}
      <div style="display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1rem;">
        <button class="cyber-button" onclick="handleSettings('${computer.id}')">
          <span class="button-content">SETTINGS</span>
        </button>
        <button 
          class="cyber-button ${computer.status === 'active' ? 'danger' : 'success'}"
          onclick="handleStartStop('${computer.id}')"
          ${computer.status === 'disconnected' ? 'disabled' : ''}
        >
          <span class="button-content">
            ${computer.status === 'active' ? 'STOP' : 'START'}
          </span>
        </button>
      </div>
    `;
    
    computerGrid.appendChild(card);
  });
}

// Action Handlers
function handleStartStop(id) {
  computers = computers.map(computer => {
    if (computer.id === id) {
      return {
        ...computer,
        status: computer.status === 'active' ? 'pending' : 'active',
        processingTime: computer.status === 'active' ? undefined : '0m'
      };
    }
    return computer;
  });
  
  renderComputers(computers);
}

function handleSettings(id) {
  console.log('Opening settings for computer:', id);
  // To be implemented
}

// Initial render
renderComputers(computers);
