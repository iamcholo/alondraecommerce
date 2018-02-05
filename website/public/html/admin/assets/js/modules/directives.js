define(['angular'],function(angular){

  angular.module('app.directives', [])
  .directive('blankDirective', [function(){}])
  .directive('showTab', function () {
    return {
      link: function (scope, element, attrs) {
        element.click(function (e) {
          e.preventDefault();
          jQuery(element).tab('show');
        });
      }
    };
  }).directive('userNav', [function() 
  {
    return{   
      templateUrl: '/admin/assets/js/modules/templates/includes/usernav.html',
      restrict: 'EC',
      replace: true
    };
  }]).directive('userSearch', [function() 
  {
    return{   
      templateUrl: '/admin/assets/js/modules/templates/includes/search.html',
      restrict: 'EC',
      replace: true
    };
  }]).directive('headerNav', [function() 
  {
    return{   
      templateUrl: '/admin/assets/js/modules/templates/includes/header.html',
      restrict: 'EC',
      replace: true
    };
  }]).directive('headingNav', [function() 
  {
    return{   
      templateUrl: '/admin/assets/js/modules/templates/includes/heading.html',
      restrict: 'EC',
      replace: true
    };
  }]).directive('sidebarNav', [function() 
  {
    return{   
      templateUrl: '/admin/assets/js/modules/templates/includes/sidebar.html',
      restrict: 'EC',
      replace: true
    };
  }]).directive('footerNav', [function() 
  {
    return{   
      templateUrl: '/admin/assets/js/modules/templates/includes/footer.html',
      restrict: 'EC',
      replace: true
    };
  }]);
  
});
