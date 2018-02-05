define(['angular','jquery'],function(angular,jquery){

      'use strict';

    angular.module('dropzone', []).
    directive('dropzone',['Media','$interval','$timeout', function(Media,$interval,$timeout) {
        return {
            templateUrl: '/admin/assets/js/modules/templates/includes/dropzone.html',
            replace: true,
            scope: { confirmAction: '&',progresss:'@'},
           
            link: function(scope, element, attrs, ngModel) {
                
                var open_uploader = function (e)
                {  
                  e.preventDefault();
                  e.stopPropagation();
                  jquery('#id_files').focus().trigger('click');
                   
                }

                element.on('click',open_uploader);
                var clicks = function(e)
                {
                    // e.preventDefault();
                     e.stopPropagation();
                }
                jquery('#id_files').on('click',clicks)
               
                jquery('#id_files').bind('change', function (e) {
                    e.stopPropagation();
                    var files = event.target.files;
                    upload(files);
                });

                element.on('drop', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                  
                    if (e.dataTransfer){
                        if (e.dataTransfer.files.length > 0) {
                            upload(e.dataTransfer.files);
                        }
                    }
                    return false;
                });
                element.on('dragover', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                });
                element.on('dragenter', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                });
                var upload = function(files) {
                    var fd = new FormData();
                    angular.forEach(files, function(value, key){
                        this.append('file', value);
                    },fd);
                 
                    var debuguploading = function(e)
                    {
                        scope.progresss = Media.uploadprogress;

                        if(Media.uploadprogress >= 100)
                        {   
                            var cancel = function()
                            {
                                $interval.cancel(stop);
                                scope.progresss = 0;
                            }
                            $timeout(cancel, 1000);                            
                        }
                    }
                    var stop = $interval(debuguploading, 10)
                    Media.New(fd).then(function successCallback(response){
                       scope.confirmAction();
                       
                    });

                };
            }
        };
        
    }]);

  
});
