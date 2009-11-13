function loader(id) {
	this.id = id;
	pai = this
	$.getJSON('/backlog/project/'+ this.id + '/',
	        function(data){
	    		pai.project = data[0];
	    		pai.sprints = data.slice(1);
	    		pai.project.ui = $('#backlogagile')
	    		pai.loadSprints(0, 5)
	        });
	
	this.loadSprints = loadSprints
	
}

function loadSprints(offset, number) {
	pai = this
	$.each(this.sprints, function(i, sprint) {
		if (i < number) {
			html = '<h1>Sprint ' + sprint.fields.number + ' - ' + sprint.fields.velocity + ' </h1>';
			html += '<ul class="sortable odd" id="sprint_' + sprint.pk + '"></ul>';
			pai.project.ui.append(html);
			sprint.ui = $('#sprint_' + sprint.pk);
			
			sprint.ui.sortable({
				axis: 'y',
				opacity: 0.7,
				connectWith: '.sortable',
				placeholder: 'ui-state-highlight',
				update: function(event, ui) {
					achou = false;
					for (z = 0; z < this.childNodes.length; z++) {
						if (this.childNodes[z] == ui.item[0]) {
							achou = true;
							break;
						}
					}
					if (achou) {
						$.post('/backlog/sprint/' + sprint.pk + '/', {'item[]': $(this).sortable('toArray')},
								function(data, textStatus) {
							for (w = 0; w < data.length; w++) {
								reload(data[w]);
							}
						}, 'json');
					}
				}
			}).disableSelection();
			
			$.getJSON('/backlog/sprint/' + sprint.pk + '/',
				function(data) {
					sprint.items = data.slice(1)
					$.each(sprint.items, function(j, item) {
						sprint.ui.append('<li class="ui-state-default" id="' + item.pk + '"></li>');
						item.ui = $('#' + item.pk);
						item.ui.load('/backlog/item/' + item.pk + '/view/', '', function(responseText, textStatus, XMLHttpRequest) {
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
						});
					});
				});
		}
	});
}

function load_sprint(slug, sprint) {
	if (sprint == 'out') {
		path = '/backlog/project/' 
	}
	
	$('#sprint_'+sprint).load('/backlog/project/' + slug + '/sprint/' + sprint + '/', '', function() {
		$('#sort_'+ sprint).sortable({
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

