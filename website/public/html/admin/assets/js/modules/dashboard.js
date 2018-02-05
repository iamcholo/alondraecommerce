require.config({
    paths: {
      "jquery": "vendor/dashboard/jquery/jquery.min",
      "jquery-migrate": "vendor/dashboard/jquery/jquery-migrate.min", 
      "jquery-ui": "vendor/dashboard/jquery/jquery-ui.min", 
      "bootstrap": "vendor/dashboard/bootstrap/bootstrap.min", 
      "moment": "vendor/dashboard/moment/moment.min", 
      "jquery_nestable": "vendor/dashboard/nestable/jquery.nestable", 
      "bootstrap_tagsinput": "vendor/dashboard/bootstrap-tagsinput/bootstrap-tagsinput", 
      "bootstrap-datetimepicker": "vendor/dashboard/bootstrap-datetimepicker/bootstrap-datetimepicker",
      "jquery-jvectormap": "vendor/dashboard/jvectormap/jquery-jvectormap.min",
      "jquery-jvectormap-world-mill-en": "vendor/dashboard/jvectormap/jquery-jvectormap-world-mill-en",
      "jquery-jvectormap-us-aea-en": "vendor/dashboard/jvectormap/jquery-jvectormap-us-aea-en", 
      "d3": "vendor/dashboard/rickshaw/d3.v3", 
      "rickshaw": "vendor/dashboard/rickshaw/rickshaw.min", 
      "bootstrap": "vendor/dashboard/bootstrap/bootstrap.min", 
      "dropzone": "vendor/dashboard/dropzone/dropzone", 
      "cropper": "vendor/dashboard/cropper/cropper.min", 
      "app_boostrap": "vendor/dashboard/app", 
      "app_plugins": "vendor/dashboard/app_plugins", 
      "app_demo": "vendor/dashboard/app_demo", 
      "app_demo_dashboard": "vendor/dashboard/app_demo_dashboard", 
    },
    baseUrl: '/admin/assets/js/',
    shim: {
      'dashboard': {
        deps: [
            'bootstrap-datetimepicker',
            'jquery-jvectormap-world-mill-en',
            'jquery-jvectormap-us-aea-en',
            'rickshaw',
            'jquery-jvectormap',
            'jquery-ui',
            'bootstrap',
            'jquery-migrate',
            'dropzone',
            'cropper',
            "jquery_nestable",
            "bootstrap_tagsinput",
            "app_boostrap",
            "app_plugins",
            "app_demo",
            "app_demo_dashboard",
        ]
      },
        'bootstrap-datetimepicker': {
            deps: ['jquery','bootstrap']
        },
        'jquery-jvectormap-world-mill-en': {
            deps: ['jquery','jquery-jvectormap']
        },

        'jquery-jvectormap-us-aea-en': {
            deps: ['jquery','jquery-jvectormap']
        },
        'rickshaw': {
            deps: ['d3']
        },
        'd3': {
            deps: ['jquery']
        },
        'jquery-jvectormap': {
            deps: ['jquery']
        },
        'jquery-ui': {
            deps: ['jquery']
        },     
        'bootstrap': {
            deps: ['bootstrap','jquery']
        },     
       'dropzone': {
            deps: ['jquery']
        },
        'cropper': {
            deps: ['jquery']
        },     

        'app_boostrap': {
            deps: ['jquery','bootstrap']
        },

        'app_plugins': {
            deps: ['jquery','bootstrap','app_boostrap']
        },

        'app_demo': {
            deps: ['jquery','bootstrap']
        },
        'app_demo_dashboard': {
            deps: ['jquery','bootstrap']
        },
        'bootstrap_tagsinput': {
          deps: ['jquery','bootstrap']
        },
        'jquery_nestable': {
            deps: ['jquery']
        },
        'bootstrap': {
            deps: ['jquery']
        },
        'jquery-migrate': {
            deps: ['jquery']
        },
    },
    deps: ['dashboard'],
    waitSeconds: 1880
});
