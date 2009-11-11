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
			$.getJSON('/backlog/sprint/' + sprint.pk + '/',
				function(data) {
					html = '<h1>Sprint ' + data[0].pk + '</h1>';
					html += '<ul class="sortable odd" id="sprint_' + data[0].pk + '"></ul>';
					pai.project.ui.append(html);
					sprint.ui = $('#sprint_' + data[0].pk);
					sprint.items = data.slice(1)
					$.each(sprint.items, function(i, item) {
						sprint.ui.append('<li class="ui-state-default" id="' + item.pk + '"></li>');
						item.ui = $('#' + item.pk);
						item.ui.load('/backlog/item/' + item.pk + '/view/');
						
					});
				});
		}
	});
}

//function moveItem(item, ) {
//	this.sprints = 
//}

