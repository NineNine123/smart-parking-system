const img = document.getElementById("parkingImage");

const canvas = document.getElementById("parkingCanvas");

const ctx = canvas.getContext("2d");

const statusText = document.getElementById("statusText");

const reader = document.getElementById("reader");

const scannerModal = document.getElementById("scannerModal");

let html5QrCode = null;

// =========================
// USER ID
// =========================

let userId = localStorage.getItem("parking_user_id");

if (!userId) {
  userId = crypto.randomUUID();

  localStorage.setItem("parking_user_id", userId);
}

// =========================
// GLOBAL DATA
// =========================

let parkingStatus = {};

let mapSlots = {};

let savedSlot = null;

let blink = false;
let selectedSlot = null;

const saveParkingModal = document.getElementById("saveParkingModal");

const modalCanvas = document.getElementById("modalParkingCanvas");

const modalImg = document.getElementById("modalParkingImage");

const modalCtx = modalCanvas.getContext("2d");

const confirmSaveBtn = document.getElementById("confirmSaveBtn");
// =========================
// PAGE LOAD
// =========================

window.onload = () => {
  setTimeout(() => {
    resizeCanvas();

    loadData();

    setInterval(loadData, 2000);
  }, 500);
};

// =========================
// WINDOW RESIZE
// =========================

window.addEventListener("resize", () => {
  resizeCanvas();

  drawParking();
});

// =========================
// RESIZE CANVAS
// =========================

function resizeCanvas() {
  canvas.width = img.offsetWidth;

  canvas.height = img.offsetHeight;
}

// =========================
// LOAD DATA
// =========================

async function loadData() {
  // parking status
  const statusResponse = await fetch("/status");

  parkingStatus = await statusResponse.json();

  // parking coordinates
  const slotsResponse = await fetch("/map_slots");

  mapSlots = await slotsResponse.json();

  drawParking();

  updateStatistics();
}

// =========================
// OPEN SAVE MODAL
// =========================

function enableSaveParkingMode() {
  saveParkingModal.style.display = "flex";

  selectedSlot = null;

  confirmSaveBtn.disabled = true;

  confirmSaveBtn.style.background = "#475569";

  confirmSaveBtn.style.opacity = "0.6";

  setTimeout(() => {
    modalCanvas.width = modalImg.offsetWidth;

    modalCanvas.height = modalImg.offsetHeight;

    drawModalParking();
  }, 100);
}

// =========================
// DRAW PARKING
// =========================

function drawParking() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const originalWidth = 1140;

  const originalHeight = 884;

  const scaleX = canvas.width / originalWidth;

  const scaleY = canvas.height / originalHeight;

  for (const slotId in mapSlots) {
    const points = mapSlots[slotId];

    const status = parkingStatus[slotId];

    // =========================
    // SLOT COLORS
    // =========================

    if (slotId === savedSlot) {
      // blinking blue effect

      if (blink) {
        ctx.fillStyle = "rgba(59,130,246,0.85)";
      } else {
        ctx.fillStyle = "rgba(59,130,246,0.25)";
      }
    } else if (status === "OCCUPIED") {
      ctx.fillStyle = "rgba(239,68,68,0.35)";
    } else {
      ctx.fillStyle = "rgba(34,197,94,0.35)";
    }

    // =========================
    // DRAW SLOT
    // =========================

    ctx.beginPath();

    ctx.moveTo(points[0][0] * scaleX, points[0][1] * scaleY);

    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(points[i][0] * scaleX, points[i][1] * scaleY);
    }

    ctx.closePath();

    ctx.fill();

    // border

    ctx.strokeStyle = "rgba(148,163,184,0.5)";

    ctx.lineWidth = 1.5;

    ctx.stroke();
  }
}
// =========================
// DRAW MODAL PARKING
// =========================

function drawModalParking() {
  modalCtx.clearRect(0, 0, modalCanvas.width, modalCanvas.height);

  const originalWidth = 1140;

  const originalHeight = 884;

  const scaleX = modalCanvas.width / originalWidth;

  const scaleY = modalCanvas.height / originalHeight;

  for (const slotId in mapSlots) {
    const points = mapSlots[slotId];

    const status = parkingStatus[slotId];

    if (slotId === selectedSlot) {
      modalCtx.fillStyle = "rgba(59,130,246,0.8)";
    } else if (status === "OCCUPIED") {
      modalCtx.fillStyle = "rgba(239,68,68,0.35)";
    } else {
      modalCtx.fillStyle = "rgba(34,197,94,0.35)";
    }

    modalCtx.beginPath();

    modalCtx.moveTo(points[0][0] * scaleX, points[0][1] * scaleY);

    for (let i = 1; i < points.length; i++) {
      modalCtx.lineTo(points[i][0] * scaleX, points[i][1] * scaleY);
    }

    modalCtx.closePath();

    modalCtx.fill();

    modalCtx.strokeStyle = "rgba(255,255,255,0.3)";

    modalCtx.stroke();
  }
}

// =========================
// SELECT SLOT IN MODAL
// =========================

modalCanvas.addEventListener(
  "click",

  (event) => {
    const rect = modalCanvas.getBoundingClientRect();

    const x = event.clientX - rect.left;

    const y = event.clientY - rect.top;

    const originalWidth = 1140;

    const originalHeight = 884;

    const scaleX = modalCanvas.width / originalWidth;

    const scaleY = modalCanvas.height / originalHeight;

    for (const slotId in mapSlots) {
      const points = mapSlots[slotId];

      modalCtx.beginPath();

      modalCtx.moveTo(points[0][0] * scaleX, points[0][1] * scaleY);

      for (let i = 1; i < points.length; i++) {
        modalCtx.lineTo(points[i][0] * scaleX, points[i][1] * scaleY);
      }

      modalCtx.closePath();

      if (modalCtx.isPointInPath(x, y)) {
        selectedSlot = slotId;

        confirmSaveBtn.disabled = false;

        confirmSaveBtn.style.background = "#10b981";

        confirmSaveBtn.style.opacity = "1";

        drawModalParking();

        break;
      }
    }
  },
);

// =========================
// CONFIRM SAVE
// =========================

async function confirmSaveParking() {
  if (!selectedSlot) return;

  await saveLocation(selectedSlot);

  closeSaveParkingModal();
}

// =========================
// CLOSE MODAL
// =========================

function closeSaveParkingModal() {
  saveParkingModal.style.display = "none";
}

// =========================
// BLINK EFFECT
// =========================

let blinkInterval = null;

// =========================
// UPDATE STATS
// =========================

function updateStatistics() {
  let occupied = 0;

  let available = 0;

  for (const slot in parkingStatus) {
    if (parkingStatus[slot] === "OCCUPIED") {
      occupied++;
    } else {
      available++;
    }
  }

  const total = occupied + available;

  const availableElement = document.getElementById("availableCount");

  const occupiedElement = document.getElementById("occupiedCount");

  const totalElement = document.getElementById("totalCount");

  if (availableElement) {
    availableElement.innerText = available;
  }

  if (occupiedElement) {
    occupiedElement.innerText = occupied;
  }

  if (totalElement) {
    totalElement.innerText = total;
  }
}

// =========================
// SAVE LOCATION
// =========================

async function saveLocation(slotId) {
  const response = await fetch("/save_location", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      user_id: userId,

      slot_id: slotId,
    }),
  });

  await response.json();

  const now = new Date();

  const time = now.toLocaleTimeString();

  statusText.innerHTML = `

    <div class="status-card success">

      <div class="status-title">
        Parking Saved
      </div>

      <div class="status-slot">
        ${slotId}
      </div>

      <div class="status-time">
        ${time}
      </div>

    </div>

  `;
}

// =========================
// FIND MY CAR
// =========================

async function getLocation() {
  const response = await fetch(`/get_location/${userId}`);

  const data = await response.json();

  if (data.slot_id) {
    savedSlot = data.slot_id;

    // stop old blinking
    if (blinkInterval) {
      clearInterval(blinkInterval);
    }

    // start blinking
    blinkInterval = setInterval(() => {
      blink = !blink;

      drawParking();
    }, 500);

    // stop after 5 seconds
    setTimeout(() => {
      clearInterval(blinkInterval);

      blink = false;

      drawParking();
    }, 5000);

    statusText.innerHTML = `

      <div class="status-card info">

        <div class="status-title">
          Car Found
        </div>

        <div class="status-slot">
          ${data.slot_id}
        </div>

        <div class="status-time">
          ${data.timestamp}
        </div>

      </div>

    `;
  } else {
    statusText.innerHTML = `

      <div class="status-card warning">

        No saved location found

      </div>

    `;
  }
}

// =========================
// START QR SCANNER
// =========================

async function startQRScanner() {
  scannerModal.style.display = "flex";

  reader.style.display = "block";

  statusText.innerHTML = `

    <div class="status-card scanning">

      Opening camera scanner...

    </div>

  `;

  html5QrCode = new Html5Qrcode("reader");

  html5QrCode
    .start(
      {
        facingMode: "environment",
      },

      {
        fps: 10,

        qrbox: 250,
      },

      async (decodedText) => {
        const parts = decodedText.split("/");

        const slotId = parts[parts.length - 1];

        statusText.innerHTML = `

        <div class="status-card success">

          QR Detected:
          ${slotId}

        </div>

      `;

        await saveLocation(slotId);

        await closeQRScanner();
      },
    )

    .catch((err) => {
      console.log(err);

      statusText.innerHTML = `

      <div class="status-card error">

        Camera access failed

      </div>

    `;
    });
}

// =========================
// CLOSE QR SCANNER
// =========================

async function closeQRScanner() {
  if (html5QrCode) {
    try {
      await html5QrCode.stop();

      await html5QrCode.clear();
    } catch (err) {
      console.log(err);
    }
  }

  reader.style.display = "none";

  scannerModal.style.display = "none";
}
