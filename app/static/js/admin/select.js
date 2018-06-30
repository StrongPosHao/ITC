//移除全部从一侧到另一侧
function sel1AddAllTosel2(srcSelectId, targetSelectId) {
	var srcSelect = document.getElementById(srcSelectId);
	var targetSelect = document.getElementById(targetSelectId);
	while (srcSelect.hasChildNodes()) {
		targetSelect.appendChild(srcSelect.firstChild);
	}
}

// 移除选中的部分从一侧到另一侧
function sel1AddTosel2(srcSelectId, targetSelectId) {
	var srcSelect = document.getElementById(srcSelectId);
	var targetSelect = document.getElementById(targetSelectId);

	var options = srcSelect.getElementsByTagName("option");
	for (var index = 0; index < options.length; index++) {
		if (options[index].selected) {
			targetSelect.appendChild(options[index]);
			index--;
		}		
	}
}