"use strict";

let fileReaders;
let fl;
let result_id;
// let result_ids;
// let preview;
// let preview_s;
// let mode;

const EXTENSIONS = ['txt', 'docx', 'pdf'];

const MODE_SINGLE = 0;
const MODE_SEPARATE = 1;

let selectedCountText = $(".selectedCountText");

let selectallBtn = $("#selectallBtn");

const api = {
	new_scan: async function(params) {
		let formData = new FormData();
		formData.append('language', params.language);
		console.log(params.files);
		[].forEach.call(params.files, (fileElement) => {
			formData.append('item_file', fileElement.files[0], '');
		});
		
		try {
			let response = await fetch('http://localhost:8080/docscanner/new_scan', {
				method: 'POST',
				body: formData
			});
		} catch (err) {
			alert(err);
		}
		
		let result = await response.json();
		
		return result.scan_id;
	},
	download: async function(params) {		
		let formData = new FormData();
		formData.append('scan_id', params.scan_id);
		formData.append('type', params.type);
		formData.append('name', params.name);
		
		let response = await fetch('http://localhost:8080/docscanner/download', {
			method: 'POST',
			body: formData
		});
		
		return await response.blob();
	}
}

function readerLoaded(e) {
	//alert(this.idx);
	let img = fileReaders[this.idx];
	img.prop("style", "background-image: url(" + e.target.result + ")");
}

function getFormMode() {
	return 0;
}

function getFormType() {
	return +document.forms.options_form.filetype_select.value;
}

function getFormName() {
	return document.getElementById('output_filename').value;
}

// --

function getFormLanguage() {
	return document.forms.options_form.language_select.value;
}

function getFormFiles() {
	return document.forms.files_form.getElementsByClassName("item_fileinput");
}

function updateSelectedCount() {
	selectedCountText.text($(".item.selected").length);
	selectallBtn.prop('disabled', !$(".item").length);
}

function init() {
	result_id = 0;
	// mode = MODE_SINGLE;
	
	fileReaders = {};
	fl = [];
	
	let mainScreen = $("#mainScreen");
	
	let images_container = $("#container_images");
	let addimageBtn = $("#addimageBtn");
	let fileselectorInput = $("#fileselectorInput");
	let removeselectedBtn = $("#removeselectedBtn");
	
	let enterselectionBtn = $("#enterselectionBtn");
	let exitselectionBtn = $("#exitselectionBtn");
	
	
	
	let outputlanguageSelect = $("#outputlanguageSelect");
	
	let downloadBtn = $("#downloadBtn");
	let previewBtn = $("#previewBtn");
	
	// let itemSelectionCheck_s = $("item_selectioncheck");
		
	$('#container_images').click(function(e) {
		if (mainScreen.hasClass('state_selection')) {
			const parent = $(e.target.parentNode);
			if (parent.hasClass('item')) {
				parent.toggleClass('selected');
			}
			updateSelectedCount();
		}
	});
	enterselectionBtn.click(function() {
		updateSelectedCount();
		
		mainScreen.toggleClass('state_normal', false); // remove state_normal
		mainScreen.toggleClass('state_selection', true); // add state_selection
	});
	exitselectionBtn.click(function() {
		mainScreen.toggleClass('state_selection', false); // remove state_selection
		mainScreen.toggleClass('state_normal', true); // add state_normal
		
		// remove all selections
		$(".item").removeClass('selected');
	});
	addimageBtn.click(function() {
		fileselectorInput.trigger("click");
	});
	fileselectorInput.change(function() {
		let new_item = $("<div>", {class: "item #col-md-4"});
		
		
		let fileinput_clone = $(this).clone();
		fileinput_clone.attr("id", "");
		fileinput_clone.attr("class", "item_fileinput");
		
		let new_item_preview = $("<div>", {class: "item_image"});
		
		
		
		let reader = new FileReader();
        reader.onload = readerLoaded;
		
		fl.push(reader);
		let last_index = fl.length - 1;
		reader.idx = last_index;
		fileReaders[last_index] = new_item_preview;
		
		
		
		
		
		
		
		let new_item_removebutton = $("<a>", {class: "item_removebutton", text: "x"});
		
		new_item.append(fileinput_clone);
		new_item.append(new_item_preview);
		new_item.append(new_item_removebutton);
		
		images_container.append(new_item);
		
	
		
		
		this.value = "";
		
		reader.readAsDataURL(fileinput_clone.get(0).files[0]);
		
		
		
		$('html, body').animate({
			scrollTop: $(document).height()
		}, 'slow');
	});
	removeselectedBtn.click(function() {
		$("#container_images .item.selected").remove();
		updateSelectedCount();
	});
	selectallBtn.click(function() {
		$("#container_images .item").addClass('selected');
		updateSelectedCount();
	});
	
	images_container.click(function(e) {
		let target = $(e.target);
		if (target.hasClass("item_removebutton")) {
			target.parent().remove();
		};
	});
	
	outputlanguageSelect.change(function(e) { // вибір іншої мови
		result_id = 0;
	});
	
	downloadBtn.click(async function() {
		if (!result_id) {
			result_id = await api.new_scan({	language: getFormLanguage(),
												files: getFormFiles()
											});
		}
		let result_blob = await api.download({
						scan_id: result_id,
						type: getFormType(),
						name: getFormName()
					 });
		
		let link = document.createElement('a');
		link.download = params.name + extensions[params.type];
		link.href = URL.createObjectURL(result_blob);
		
		link.click();
		
		URL.revokeObjectURL(link.href);
	});
}