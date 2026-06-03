document.addEventListener("DOMContentLoaded", () => {
    const dashboardWrapper = document.querySelector('.booking-dashboard-wrapper');
    if (!dashboardWrapper) {
        return;
    }

    console.log("booking.js loaded safely on dashboard");

    window.addEventListener("error", (e) => {
        console.error("Global JS Error:", e.error);
    });

    const captainSearch = document.querySelector("#captain_search");
    const captainHidden = document.querySelector("#captain");
    const teammatesContainer = document.querySelector("#teammates-container");
    const addTeammateBtn = document.querySelector("#add-teammate-btn");
    const dateInput = document.querySelector("#date");
    const submitBtn = document.querySelector("#submitBtn");

    const warningBanner = document.querySelector("#js-warning-banner");
    const warningMessage = document.querySelector("#js-warning-message");
    const masterDatalist = document.querySelector("#player-search-list");

    if (dateInput && dateInput.value) {
        dateInput.min = dateInput.value;
    }

    function showTopWarning(msg) {
        if (warningMessage && warningBanner) {
            warningMessage.innerHTML = msg;
            warningBanner.style.display = "block";

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        } else {
            console.warn("System Notice:", msg);
            alert(msg.replace(/<\/?[^>]+(>|$)/g, ""));
        }
    }

    function clearTopWarning() {
        if (warningMessage && warningBanner) {
            warningMessage.innerHTML = "";
            warningBanner.style.display = "none";
        }
    }

    function getOptionIdByValue(val) {
        if (!masterDatalist || !val) return null;
        const normalized = val.trim().toLowerCase();

        const option = Array.from(masterDatalist.options).find(opt => {
            return opt && opt.value && opt.value.trim().toLowerCase() === normalized;
        });

        return option ? option.dataset.id : null;
    }

    function getOptionValueById(id) {
        if (!masterDatalist || !id) return "";

        const option = Array.from(masterDatalist.options).find(opt => {
            return opt && opt.dataset && String(opt.dataset.id) === String(id);
        });

        return option ? option.value : "";
    }

    async function checkAvailability(userId, date) {
        if (!userId || !date) {
            return { available: true };
        }
        try {
            const response = await fetch(`/api/check-player/?user_id=${userId}&date=${date}`);
            if (!response.ok) return { available: true };
            return await response.json();
        } catch (error) {
            console.error("Availability API Error:", error);
            return { available: true };
        }
    }

    function updateAddButtonState() {
        if (!addTeammateBtn || !teammatesContainer) return;

        const currentTeammateCount = teammatesContainer.querySelectorAll(".teammate-row").length;

        if (currentTeammateCount >= 9) {
            addTeammateBtn.disabled = true;
            addTeammateBtn.style.opacity = "0.5";
            addTeammateBtn.style.cursor = "not-allowed";
        } else {
            addTeammateBtn.disabled = false;
            addTeammateBtn.style.opacity = "1";
            addTeammateBtn.style.cursor = "pointer";
        }
    }

    if (captainSearch) {
        captainSearch.addEventListener("input", async () => {
            clearTopWarning();
            if (submitBtn) submitBtn.disabled = false;

            const val = captainSearch.value;
            const matchedId = getOptionIdByValue(val);

            if (!matchedId) {
                if (captainHidden) captainHidden.value = "";
                return;
            }

            if (captainHidden) captainHidden.value = matchedId;

            const selectedDate = dateInput ? dateInput.value : "";
            const statusData = await checkAvailability(matchedId, selectedDate);
            const captainName = val.split("(")[0].trim();

            if (!statusData.available) {
                if (statusData.reason === "banned") {
                    showTopWarning(`🚫 <strong>Account Suspended:</strong> ${captainName} is banned.`);
                } else {
                    showTopWarning(`🚫 <strong>Selection Blocked:</strong> ${captainName} is already booked on ${selectedDate}.`);
                }

                captainSearch.value = "";
                if (captainHidden) captainHidden.value = "";
                if (submitBtn) submitBtn.disabled = true;
            }
        });
    }

    if (addTeammateBtn) {
        addTeammateBtn.addEventListener("click", () => {
            clearTopWarning();
            if (!teammatesContainer) return;

            const currentTeammateCount = teammatesContainer.querySelectorAll(".teammate-row").length;
            if (currentTeammateCount >= 9) {
                showTopWarning(`⚠️ <strong>Roster Limit Reached:</strong> Max 9 teammates allowed.`);
                return;
            }

            const row = document.createElement("div");
            row.className = "teammate-row";

            const textInput = document.createElement("input");
            textInput.type = "text";
            textInput.placeholder = "🔍 Search teammate...";
            textInput.setAttribute("list", "player-search-list");
            textInput.required = true;
            textInput.style.marginTop = "5px";

            const hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "teammates";

            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.className = "btn-remove";
            removeBtn.innerText = "✕";
            removeBtn.style.marginTop = "5px";

            row.appendChild(textInput);
            row.appendChild(hiddenInput);
            row.appendChild(removeBtn);
            teammatesContainer.appendChild(row);

            updateAddButtonState();

            textInput.addEventListener("input", async () => {
                clearTopWarning();
                const val = textInput.value;
                const matchedId = getOptionIdByValue(val);

                if (!matchedId) {
                    hiddenInput.value = "";
                    return;
                }

                hiddenInput.value = matchedId;
                const selectedDate = dateInput ? dateInput.value : "";
                const currentCaptainId = captainHidden ? captainHidden.value : "";
                const playerName = val.split("(")[0].trim();

                if (matchedId === currentCaptainId) {
                    showTopWarning(`⚠️ <strong>Action Blocked:</strong> User already selected as Captain.`);
                    textInput.value = "";
                    hiddenInput.value = "";
                    return;
                }

                const allHiddenInputs = Array.from(teammatesContainer.querySelectorAll("input[type='hidden']"));
                const duplicates = allHiddenInputs.filter(h => h !== hiddenInput && h.value === matchedId);

                if (duplicates.length > 0) {
                    showTopWarning(`⚠️ <strong>Duplicate Entry:</strong> Teammate already added.`);
                    textInput.value = "";
                    hiddenInput.value = "";
                    return;
                }

                const statusData = await checkAvailability(matchedId, selectedDate);
                if (!statusData.available) {
                    if (statusData.reason === "banned") {
                        showTopWarning(`🚫 <strong>Line-up Error:</strong> ${playerName} is banned.`);
                    } else {
                        showTopWarning(`🚫 <strong>Line-up Error:</strong> ${playerName} already has a booking on ${selectedDate}.`);
                    }
                    textInput.value = "";
                    hiddenInput.value = "";
                }
            });

            removeBtn.addEventListener("click", () => {
                row.remove();
                clearTopWarning();
                updateAddButtonState();
            });
        });
    }

    if (dateInput) {
        dateInput.addEventListener("change", () => {
            clearTopWarning();
            if (captainHidden && captainHidden.value && captainSearch) {
                captainSearch.dispatchEvent(new Event("input", { bubbles: true }));
            }
            if (teammatesContainer) teammatesContainer.innerHTML = "";
            updateAddButtonState();
        });
    }

    if (captainHidden && captainSearch) {
        const loggedUserId = captainHidden.getAttribute("data-logged-user-id");
        console.log("Logged User ID from context attributes:", loggedUserId);

        if (loggedUserId && loggedUserId !== "None" && loggedUserId !== "") {
            const initialValue = getOptionValueById(loggedUserId);
            console.log("Found dropdown string sequence target:", initialValue);

            if (initialValue) {
                captainSearch.value = initialValue;
                captainHidden.value = loggedUserId;

                const selectedDate = dateInput ? dateInput.value : "";
                checkAvailability(loggedUserId, selectedDate).then(statusData => {
                    if (statusData && !statusData.available) {
                        const captainName = initialValue.split("(")[0].trim();
                        if (statusData.reason === "banned") {
                            showTopWarning(`🚫 <strong>Account Suspended:</strong> ${captainName} is banned.`);
                        } else {
                            showTopWarning(`🚫 <strong>Selection Blocked:</strong> ${captainName} is already booked.`);
                        }
                        if (submitBtn) submitBtn.disabled = true;
                    }
                });
            }
        }
    }

    updateAddButtonState();
});
