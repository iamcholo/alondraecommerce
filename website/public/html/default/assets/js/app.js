$(function() {

		var navigations = $("#navigation .dropdown, #top_nav .dropdown");

		disable_navitation = function ()
		{
			child = navigations.find('a[data-toggle=dropdown]');
			child.removeClass('disabled');
		}

		enable_hover_effect = function()
		{
			child = navigations.find('a[data-toggle=dropdown]')
			child_child = child.find('i.pull-right');
			
			open_nav = function (current, parent) 
			{ 
				current.removeClass('fa-caret-right');
				current.addClass('fa-caret-down');
			}

			hive_nav = function (current, parent) 
			{ 				
				current.removeClass('fa-caret-down');
				current.addClass('fa-caret-right');
			}

			click_nav = function (e)
			{
				var current = $(this);
				var parent = current.parent().parent();
				parent.toggleClass('open');
				if (parent.hasClass('open'))
				{
					open_nav(current, parent);
				}
				else
				{
					hive_nav(current, parent);
				}
				return false;
			}

			focus_out = function(e)
			{
				var parent = $(this);
				var child = parent.find('a[data-toggle=dropdown]');
				var current = child.find('i.pull-right');
				if (!parent.hasClass('open'))
				{
					current.removeClass('fa-caret-down');
					current.addClass('fa-caret-right');				
				}
			}

			child_child.on('click', click_nav);
			navigations.on('hidden.bs.dropdown', focus_out);
		}
		enable_hover_effect();
});