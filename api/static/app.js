const endpoints = {
  lock: { method: "POST", url: "/vehicle/lock" },
  unlock: { method: "POST", url: "/vehicle/unlock" },
  wake: { method: "POST", url: "/vehicle/wake" },
  sleep: { method: "POST", url: "/vehicle/sleep" },
  "charge-start": { method: "POST", url: "/vehicle/charge/start" },
  "charge-step": { method: "POST", url: "/vehicle/charge/step" },
  "charge-stop": { method: "POST", url: "/vehicle/charge/stop" },
  "climate-stop": { method: "POST", url: "/vehicle/climate/stop" },
  "window-open": { method: "POST", url: "/vehicle/window/open" },
  "window-close": { method: "POST", url: "/vehicle/window/close" },
  "window-vent": { method: "POST", url: "/vehicle/window/vent" },
  "fault-clear": { method: "DELETE", url: "/vehicle/faults" },
  reset: { method: "POST", url: "/vehicle/reset" },
};

const statusTemplate = document.querySelector("#statusTemplate");
const statusGrid = document.querySelector("#statusGrid");
const eventLog = document.querySelector("#eventLog");
const windowInput = document.querySelector("#windowInput");
const windowValue = document.querySelector("#windowValue");
const targetTempInput = document.querySelector("#targetTempInput");
const gearSelect = document.querySelector("#gearSelect");
const faultField = document.querySelector("#faultField");
const faultValue = document.querySelector("#faultValue");
const verificationSteps = document.querySelector("#verificationSteps");
const runVerificationButton = document.querySelector("#runVerificationButton");
const verificationState = document.querySelector("#verificationState");

let currentState = null;

function formatBoolean(value, truthy, falsy) {
  return value ? truthy : falsy;
}

function formatTemp(value) {
  return value === null || value === undefined ? "Off" : `${value} F`;
}

function setPill(id, text, tone) {
  const node = document.querySelector(id);
  node.textContent = text;
  node.className = `pill ${tone || ""}`.trim();
}

function addEvent(message, isError = false) {
  const entry = document.createElement("div");
  entry.className = isError ? "event error" : "event";
  entry.textContent = `${new Date().toLocaleTimeString()} - ${message}`;
  eventLog.prepend(entry);

  while (eventLog.children.length > 40) {
    eventLog.removeChild(eventLog.lastElementChild);
  }
}

function renderStatusCard(label, value) {
  const card = statusTemplate.content.firstElementChild.cloneNode(true);
  card.querySelector(".status-label").textContent = label;
  card.querySelector(".status-value").textContent = value;
  statusGrid.appendChild(card);
}

function renderState(state) {
  currentState = state;
  statusGrid.replaceChildren();

  const failures = state.detected_failures || [];
  renderStatusCard("Doors", formatBoolean(state.locked, "Locked", "Unlocked"));
  renderStatusCard("Awake", formatBoolean(state.awake, "Awake", "Asleep"));
  renderStatusCard("Battery", `${state.battery_percentage}%`);
  renderStatusCard("Charging", formatBoolean(state.charging, "Charging", "Idle"));
  renderStatusCard("Climate", formatBoolean(state.climate_control_on, "On", "Off"));
  renderStatusCard("Target", formatTemp(state.target_temp));
  renderStatusCard("Gear", state.transmission);
  renderStatusCard("Window", `${state.window}%`);

  setPill("#doorState", formatBoolean(state.locked, "Locked", "Unlocked"), state.locked ? "ok" : "warn");
  setPill("#awakeState", formatBoolean(state.awake, "Awake", "Asleep"), state.awake ? "ok" : "warn");
  setPill("#batteryState", `${state.battery_percentage}%`, state.battery_percentage > 20 ? "ok" : "bad");
  setPill("#climateState", formatBoolean(state.climate_control_on, "On", "Off"), state.climate_control_on ? "ok" : "");
  setPill("#windowState", `${state.window}%`, state.window > 0 ? "warn" : "ok");
  setPill("#gearState", state.transmission, state.transmission === "P" ? "ok" : "warn");
  setPill("#faultState", failures.length ? `${failures.length} detected` : "Clear", failures.length ? "bad" : "ok");
  setPill("#lastUpdated", new Date().toLocaleTimeString(), "");

  document.querySelector("#lockBadge").textContent = formatBoolean(state.locked, "Locked", "Unlocked");
  document.querySelector("#climateBadge").textContent = formatBoolean(state.climate_control_on, `Climate ${formatTemp(state.target_temp)}`, "Climate off");
  document.querySelector("#windowFill").style.transform = `scaleY(${Number(state.window) / 100})`;

  windowInput.value = state.window;
  windowValue.textContent = `${state.window}%`;
  if (state.target_temp !== null && state.target_temp !== undefined) {
    targetTempInput.value = state.target_temp;
  }
  gearSelect.value = state.transmission;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Command failed");
  }
  return payload;
}

async function refreshState(logMessage) {
  const payload = await requestJson("/vehicle/state");
  renderState(payload.state);
  if (logMessage) {
    addEvent(logMessage);
  }
  return payload.state;
}

function commandPayload(commandName) {
  if (commandName === "climate-start") {
    return {
      method: "POST",
      url: "/vehicle/climate/start",
      body: { target_temp: Number(targetTempInput.value) },
    };
  }

  if (commandName === "window-set") {
    return {
      method: "POST",
      url: "/vehicle/window/set",
      body: { percentage: Number(windowInput.value) },
    };
  }

  if (commandName === "gear-shift") {
    return {
      method: "POST",
      url: "/vehicle/transmission/shift",
      body: { gear: gearSelect.value },
    };
  }

  if (commandName === "fault-inject") {
    return {
      method: "POST",
      url: "/vehicle/faults",
      body: { field: faultField.value, value: parseFaultValue(faultValue.value) },
    };
  }

  return endpoints[commandName];
}

function parseFaultValue(value) {
  const trimmed = value.trim();
  if (trimmed.toLowerCase() === "true") return true;
  if (trimmed.toLowerCase() === "false") return false;
  if (trimmed.toLowerCase() === "null") return null;
  if (trimmed !== "" && !Number.isNaN(Number(trimmed))) return Number(trimmed);
  return trimmed;
}

async function runCommand(commandName, label) {
  const config = commandPayload(commandName);
  if (!config) return;

  const options = { method: config.method };
  if (config.body !== undefined) {
    options.body = JSON.stringify(config.body);
  }

  const payload = await requestJson(config.url, options);
  renderState(payload.state);
  addEvent(payload.message || label || "Command completed");
  return payload.state;
}

async function handleCommand(event) {
  const button = event.target.closest("[data-command]");
  if (!button) return;

  button.disabled = true;
  try {
    await runCommand(button.dataset.command, button.textContent.trim());
  } catch (error) {
    addEvent(error.message, true);
  } finally {
    button.disabled = false;
  }
}

function setVerificationStep(index, tone) {
  const item = verificationSteps.children[index];
  if (item) item.className = tone;
}

async function runVerification() {
  const sequence = [
    ["Reset", "reset"],
    ["Lock doors", "lock"],
    ["Unlock doors", "unlock"],
    ["Start climate", "climate-start"],
    ["Set window 50%", "window-set"],
    ["Shift to drive", "gear-shift"],
    ["Start charging", "charge-start"],
    ["Simulate charge step", "charge-step"],
    ["Stop charging", "charge-stop"],
    ["Close window", "window-close"],
    ["Stop climate", "climate-stop"],
    ["Shift to park", "gear-shift"],
    ["Sleep", "sleep"],
    ["Wake", "wake"],
  ];

  verificationSteps.replaceChildren(
    ...sequence.map(([label]) => {
      const item = document.createElement("li");
      item.textContent = label;
      return item;
    })
  );

  runVerificationButton.disabled = true;
  verificationState.textContent = "Running";
  verificationState.className = "pill warn";

  try {
    for (let index = 0; index < sequence.length; index += 1) {
      const [label, command] = sequence[index];
      if (label === "Set window 50%") windowInput.value = 50;
      if (label === "Shift to drive") gearSelect.value = "D";
      if (label === "Shift to park") gearSelect.value = "P";

      await runCommand(command, label);
      setVerificationStep(index, "pass");
    }

    verificationState.textContent = "Passed";
    verificationState.className = "pill ok";
  } catch (error) {
    const failedIndex = [...verificationSteps.children].findIndex((item) => item.className !== "pass");
    setVerificationStep(failedIndex, "fail");
    verificationState.textContent = "Failed";
    verificationState.className = "pill bad";
    addEvent(error.message, true);
  } finally {
    runVerificationButton.disabled = false;
  }
}

document.addEventListener("click", handleCommand);
document.querySelector("#refreshButton").addEventListener("click", () => refreshState("State refreshed").catch((error) => addEvent(error.message, true)));
document.querySelector("#resetButton").addEventListener("click", () => runCommand("reset", "Vehicle reset").catch((error) => addEvent(error.message, true)));
runVerificationButton.addEventListener("click", runVerification);
windowInput.addEventListener("input", () => {
  windowValue.textContent = `${windowInput.value}%`;
});

refreshState("Console connected").catch((error) => addEvent(error.message, true));
