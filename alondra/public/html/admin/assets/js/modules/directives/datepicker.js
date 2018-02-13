define(['angular','jquery'],function(angular,jquery){

      'use strict';

    angular.module('datepicker', []).

    directive('datepicker', function () {
        return {
         
            
            replace: true,
            scope : {
              ngModel : '=',
              ngId : '@' ,
            },            

            templateUrl: '/admin/assets/js/modules/templates/includes/datepicker.html',
            link: function($scope, elem, attr, ctrl) {

            },
            controller: ['$scope','$timeout', function ($scope,$timeout) {
               var c =function(){

                  jquery('#datetimepicker_'+$scope.ngId).datetimepicker({
                    viewMode: 'years',
                    format: 'YYYY-MM-DD H:mm:ss'
                    }).on("dp.change", function (e) {
                    $scope.ngModel  = jquery('#datetimepicker_'+$scope.ngId+' input').val();
                });

               }
               $timeout(c,500)

              
            
            }]

        }
    });

  
});
