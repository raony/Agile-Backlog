function load_sprint(slug, sprint) {
	$sprint = $('#sprint_'+sprint);
	$sprint.find('.sortable').hide();
	$sprint.parent().find(".loader").show();
	$sprint.load('/backlog/project/' + slug + '/sprint/' + sprint + '/', '', function() {
		sortable = $('#sort_' + sprint);
		sortable.show();
		sortable.parent().parent().find(".loader").hide();
		sortable.sortable({
			axis: 'y',
			opacity: 0.7,
			connectWith: '.sortable',
			placeholder: 'ui-state-highlight',
			update: function(event, ui) {
				found = false;
				for (z = 0; z < this.childNodes.length; z++) {
					if (this.childNodes[z] == ui.item[0]) {
						found = true;
						break;
					}
				}
				if (found) {
					$.post('/backlog/project/' + slug + '/sprint/' + sprint + '/', {'item[]': $(this).sortable('toArray')},
						function(data, textStatus) {
							for (w = 0; w < data.length; w++) {
								load_sprint(slug, data[w]);
							}
						}, 'json');
				}
			}
		}).disableSelection();
	});
}

function load_items(sortable, items) {
	for (i = 0; i < items.length; i++) {
		sortable.find('#' + items[i]).load('/backlog/item/' + items[i] + '/view/', '', 
				function(responseText, textStatus, XMLHttpRequest) {
//				sortable.parent().parent().find(".loader").hide();
				$(this).find(".description").hide();
				$(this).find(".toggledescription").click(function() {
					var o = $(this);
					$(this).parent().find(".description").toggle(0, function() {
						if ($(this).is(":visible")) {
							o.addClass("toggleback");
							o.find("span").text("Ocultar");
						} else {
							o.removeClass("toggleback");
							o.find("span").text("Exibir");
						}
					});
				});
				$(this).show()
		});
	}	
}

function isBottom() {
	var scr;
	var height = $(document).height() - $(window).height() - 50;

	if (navigator.appName == "Microsoft Internet Explorer") {
		scr = document.body.scrollTop;
	} else {
		scr = window.pageYOffset;
	}
	if (scr >= height) {
	    return true;
	}
}

$(document).ready(function() {
	$(".description").hide();
	
	$(".toggledescription").click(function() {
		var o = $(this);
		$(this).parent().find(".description").toggle(0, function() {
			if ($(this).is(":visible")) {
				o.addClass("toggleback");
				o.find("span").text("Ocultar");
			} else {
				o.removeClass("toggleback");
				o.find("span").text("Exibir");
			}
			o.attr("title", o.text());
		});
	});

	$(".sortable li h2").dblclick(function() {
		$(this).parent().find(".toggledescription").click();
	});
});

/*
$(window).scroll(function() {
	if (isBottom()) {
		alert("chegou no fim.");
	}
});
*/

