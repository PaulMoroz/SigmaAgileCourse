"use strict";

let fileReaders;
let fl;
let result_id;
let result_ids;
let preview;
let preview_s;
let mode;

const MODE_SINGLE = 0;
const MODE_SEPARATE = 1;

function readerLoaded(e) {
	//alert(this.idx);
	let img = fileReaders[this.idx];
	img.prop("src", e.target.result);
};

function init() {
	result_id = 0;
	result_ids = [];
	preview = false;
	preview_s = false;
	mode = MODE_SINGLE;
	
	fileReaders = {};
	fl = [];
	
	let mainScreen = $("#mainScreen");
	
	let images_container = $("#container_images");
	let addimageBtn = $("#addimageBtn");
	let fileselectorInput = $("#fileselectorInput");
	let removeselectedBtn = $("#removeselectedBtn");
	
	let enterselectionBtn = $("#enterselectionBtn");
	let exitselectionBtn = $("#exitselectionBtn");
	
	let selectallBtn = $("#selectallBtn");
	
	let outputlanguageSelect = $("#outputlanguageSelect");
	
	let downloadBtn = $("#downloadBtn");
	let previewBtn = $("#previewBtn");
	
	enterselectionBtn.click(function() {
		mainScreen.toggleClass("state_normal", false); // remove state_normal
		mainScreen.toggleClass("state_selection", true); // add state_selection
	});
	exitselectionBtn.click(function() {
		// remove all selections
		$("#container_images .item_selectioncheck").prop("checked", false);
		
		mainScreen.toggleClass("state_selection", false); // remove state_selection
		mainScreen.toggleClass("state_normal", true); // add state_normal
	});
	addimageBtn.click(function() {
		fileselectorInput.trigger("click");
	});
	fileselectorInput.change(function() {
		let new_item = $("<div>", {class: "item"});
		
		
		let fileinput_clone = $(this).clone();
		fileinput_clone.attr("id", "");
		
		let new_item_preview = $("<img>", {src: ""});
		
		
		
		let reader = new FileReader();
        reader.onload = readerLoaded;
		
		fl.push(reader);
		let last_index = fl.length - 1;
		reader.idx = last_index;
		fileReaders[last_index] = new_item_preview;
		
		
		
		
		
		
		
		let new_item_removebutton = $("<a>", {class: "item_removebutton", text: "x"});
		
		let new_item_selectioncheck = $("<input>", {type: "checkbox", class: "item_selectioncheck"});
		
		new_item.append(fileinput_clone);
		new_item.append(new_item_preview);
		new_item.append(new_item_removebutton);
		new_item.append(new_item_selectioncheck);
		
		images_container.append(new_item);
		
	
		
		
		this.value = "";
		
		reader.readAsDataURL(fileinput_clone.get(0).files[0]);
	});
	removeselectedBtn.click(function() {
		$("#container_images .item").each(function(index, value) {
			if ($(this).find(".item_selectioncheck").prop("checked")) {
				$(this).remove();
			};
		});
	});
	selectallBtn.click(function() {
		// check all selections
		$("#container_images .item_selectioncheck").prop("checked", true);
	});
	
	images_container.click(function(e) {
		let target = $(e.target);
		if (target.hasClass("item_removebutton")) {
			target.parent().remove();
		};
	});
	
	outputlanguageSelect.change(function(e) { // вибір іншої мови
		result_id = 0;
		result_ids.clear();
		preview = false;
		preview_s = false;
	});
	
	downloadBtn.click(function() {
		if (mode) { // separate mode
			if (result_ids.length == 0) {
				result_ids = my_api_newscan_separate();
			}
			my_api_download_zip();
		} else { // single mode
			if (result_id == 0) {
				result_id = my_api_newscan();
			}
			my_api_download();
		}
	});
}