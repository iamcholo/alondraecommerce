define(['angular','SimpleMDE'],function(angular,SimpleMDE){

      'use strict';

    angular.module('cms-simplemde', []).

    service('simplemde', [function(){
        this.css_url = '/admin/assets/css/simplemde.css';
        this.isAlreadyLoaded = false;
    }]).

    directive('simplemde', function () {
        return {
         
            
            replace: true,
            scope : {
              ngModel : '=',
              confirmAction: '&',
            },            

            template: '<div><textarea " ng-model="ngModel" class="form-control" id="content"  cols="40" rows="10" ></textarea></div>',
            link: function($scope, elem, attr, ctrl) {

               
             
            },
            controller: ['simplemde','$scope','$timeout', function (simplemde,$scope,$timeout) {
               
               // $timeout( function()
            //{



                if(!simplemde.isAlreadyLoaded)
                {
                      var element = document.createElement("link");
                      element.setAttribute("rel", "stylesheet");
                      element.setAttribute("type", "text/css");
                      element.setAttribute("href", simplemde.css_url);
                      document.getElementsByTagName("head")[0].appendChild(element);
                      simplemde.isAlreadyLoaded = true;
                  }

                 var toolbar = [
                        {
                            name: "toggleBold",
                            action: SimpleMDE.toggleBold,
                            className: "fa fa-bold", // Look for a suitable icon
                            title: "bold (Cmd-B)",
                        },
                        {
                            name: "toggleItalic",
                            action: SimpleMDE.toggleItalic,
                            className: "fa fa-italic", // Look for a suitable icon
                            title: "italic (Cmd-I)",
                        },
                        {
                            name: "drawLink",
                            action: SimpleMDE.drawLink,
                            className: "fa fa-link", // Look for a suitable icon
                            title: "link (Cmd-K)",
                        },
                        {
                            name: "toggleHeadingSmaller",
                            action: SimpleMDE.toggleHeadingSmaller,
                            className: "fa fa fa-header", // Look for a suitable icon
                            title: "heading-smaller",
                        },
                        {
                            name: "toggleHeadingBigger",
                            action: SimpleMDE.toggleHeadingBigger,
                            className: "fa fa fa-header", // Look for a suitable icon
                            title: "heading-bigger",
                        },
                        {
                            name: "cleanBlock",
                            action: SimpleMDE.cleanBlock,
                            className: "fa fa-eraser fa-clean-block", // Look for a suitable icon
                            title: "clean-block",
                        },
                        {
                            name: "drawImage",
                            action: SimpleMDE.drawImage,
                            className: "fa fa-picture-o", // Look for a suitable icon
                            title: "image",
                        },
                        {
                            name: "toggleBlockquote",
                            action: SimpleMDE.toggleBlockquote,
                            className: "fa fa-quote-left", // Look for a suitable icon
                            title: "quote",
                        },
                        {
                            name: "toggleOrderedList",
                            action: SimpleMDE.toggleOrderedList,
                            className: "fa fa-list-ol", // Look for a suitable icon
                            title: "link",
                        },
                        {
                            name: "toggleUnorderedList",
                            action: SimpleMDE.toggleUnorderedList,
                            className: "fa fa-list-ul", // Look for a suitable icon
                            title: "ordered-list",
                        },
                        {
                            name: "toggleUnorderedList",
                            action: SimpleMDE.toggleUnorderedList,
                            className: "fa fa-list-ul", // Look for a suitable icon
                            title: "unordered-list",
                        },
                        {
                            name: "toggleCodeBlock",
                            action: SimpleMDE.toggleCodeBlock,
                            className: "fa fa-code", // Look for a suitable icon
                            title: "code",
                        },
                        {
                            name: "togglePreview",
                            action: SimpleMDE.togglePreview,
                            className: "fa fa-eye", // Look for a suitable icon
                            title: "preview",
                        },
                        {
                            name: "toggleSideBySide",
                            action: SimpleMDE.toggleSideBySide,
                            className: "fa fa-columns", // Look for a suitable icon
                            title: "side-by-side",
                        },
                        {
                            name: "toggleFullScreen",
                            action: SimpleMDE.toggleFullScreen,
                            className: "fa fa-arrows-alt", // Look for a suitable icon
                            title: "fullscreen",
                        }
                      ];

                      var shortcuts = {
                        "toggleBold": "Cmd-B",
                        "toggleItalic": "Cmd-I",
                        "drawLink": "Cmd-K",
                        "toggleHeadingSmaller": "Cmd-H",
                        "toggleHeadingBigger": "Shift-Cmd-H",
                        "cleanBlock": "Cmd-E",
                        "drawImage": "Cmd-Alt-I",
                        "toggleBlockquote": "Cmd-'",
                        "toggleOrderedList": "Cmd-Alt-L",
                        "toggleUnorderedList": "Cmd-L",
                        "toggleCodeBlock": "Cmd-Alt-C",
                        "togglePreview": "Cmd-P",
                        "toggleSideBySide": "F9",
                        "toggleFullScreen": "F11"
                      };
                        function CreateEditor(data)
                        {

                             var myEditor = new SimpleMDE({
                                    toolbar: toolbar,
                                    element:document.getElementById("content"),
                                    spellChecker: false,
                                })

                                myEditor.value( data);
                                myEditor.codemirror.on("change", function(){
                                    $scope.ngModel = myEditor.value();
                                });
                        }


                            try{
                              
                                $scope.confirmAction().then(function successCallback(response){                          
                                    CreateEditor( response.data.content);
                                });
                            }
                            catch(e){
                                CreateEditor($scope.ngModel);
                            };
                     
                   

           // } ,1000)
          

            
            }]

        }
    });

  
});
