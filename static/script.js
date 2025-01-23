document.querySelector("#more").addEventListener("click", () => {
	document.querySelector("#additional-info").classList.remove("hidden");
	document.querySelector("#less").classList.remove("hidden")
	document.querySelector("#more").classList.add("hidden")
});
document.querySelector("#less").addEventListener("click", () => {
	document.querySelector("#additional-info").classList.add("hidden");
	document.querySelector("#less").classList.add("hidden")
	document.querySelector("#more").classList.remove("hidden")
});
