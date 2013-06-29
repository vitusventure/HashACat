function getCat (hash) {
	window.location.href = 'http://hashacat.com/cat/' + hash;
}

function getRandomCat () {
	$.getJSON('http://hashacat.com/randomHash', function(data) {
		getCat(data.hash);
	});
}

function textToHash (hashText) {
	var hashText = hashText.substring(0,255);
	encodedHashText = window.btoa(hashText);
	$.getJSON('http://hashacat.com/hash/' + encodedHashText, function(data) {
		getCat(data.hash);
	});
}

$(document).ready(function () {
	$('#hashCatForm').submit(function (e) {
		hashVal = $("#hashInput").val();

		if (!hashVal) {
			getRandomCat();
		} else if (hashVal.match(/^([a-f0-9]{40})$|^([a-f0-9]{32})$/)) {
			getCat(hashVal);
		} else {
			textToHash(hashVal);
		}

		e.preventDefault();
		return false;
	});
});

