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
	$.each(this.sprints, function(i, item) {
		if (i < number) {
			$.getJSON('/backlog/sprint/' + item.id + '/',
				function(data) {
					html = '<h1>Sprint ' + data[0].pk + '</h1>';
					html += '<ul class="sortable odd" id="sprint_' + data[0].pk + '"></ul>';
					pai.project.ui.append(html)
					item.ui = $('#sprint_' + data[0].pk)
					//for (item in data[1]) {
					//	html += '<li class="ui-state-default" id="' + item.pk + '">' + {% item_show item %} + '</li>'
					//}
						
				});
			pai.project.ui.
		}
	});
}

function sprintHTML(sprint) {
	sprint = new Object;
	
	
}