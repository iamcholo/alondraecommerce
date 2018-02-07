define(['angular'],function(angular){
    angular.module('app.I18N.ES', [])
    .config(['$translateProvider', function ($translateProvider) 
    {
        $translateProvider.translations('es', {
            'TITLE_LABEL': 'Titulo',
            'THUMBNAIL_LABEL':'Miniatura',
            'THUMBNAIL_TEXT_LABEL':'Miniatura Texto',
            'FEATURED_IMAGE_LABEL':'Imagen Descatada',
            'FEATURED_IMAGE_TEXT_LABEL':'Imagen Descatada Texto',
            'FILE_PLURAL_LABEL': 'Archivos',
            'LIST_LABEL': 'Lista',
            'EDIT_LABEL': 'Editar',
            'NEW_LABEL': 'Nuevo',
            'DELETE_LABEL': 'Borrar',
            'UPDATE_LABEL': 'Actualizar',
            'ACTIONS_LABEL': 'Acciones',
            'CREATED_LABEL': 'Created',
            'UPDATED_LABEL': 'Updated',
            'THUMB_LABEL': 'Thumb',
            'PUBLISHED_LABEL': 'Publicado',
            'SAVE_LABEL': 'Guardar',
            'POST_LABEL': 'Post',
            'POST_PLURAL_LABEL': 'Posts',
            'SEARCH_LABEL': 'Buscar', 
            'CONTENT_LABEL': 'Contenido',  
            'CATEGORIES_LABEL': 'Categorias',
            'MEDIA_LABEL': 'Media',  
            'IMAGE_LABEL': 'Imagen',
            'MEDIA_EXTERNAL_LABEL': 'Media External', 
            'THUMBNAIL_LABEL': 'Miniatura',  
            'FEATURED_LABEL': 'Destacado',  
            'SEARCH_FOR_LABEL': 'Deseo buscar...',  
            'IMAGE_PLURAL_LABEL': 'Imagenes',
            'USER_PLURAL_LABEL': 'Usuarios',  
            'USER_LABEL': 'Usuario', 
            'FIRST_NAME_LABEL': 'Primer Nombre',
            'LAST_NAME_LABEL': 'Segundo Nombre',
            'COMPANY_NAME_LABEL': 'Compañia',
            'EMAIL_NAME_LABEL': 'Email',
            'NICK_NAME_LABEL': 'Nick',
            'ADDRESS_LABEL': 'Direccion',
            'ADDRESS_LINE_2_LABEL': 'Direccion linea 2',
            'SELECT_COUNTRY_LABEL': 'Seleccionar Pais',
            'ZIP_CODE_LABEL': 'Codigo Postal',
            'WEBSITE_LABEL': 'Sitio web',
            'JOB_POSITION_LABEL': 'Cargo que Ocupa en su empresa',
            'JOB_DESCRIPTION_LABEL': 'Breve Descripcion',
            'MOBILE_PHONE_LABEL': 'Numero Celular',
            'DESCRIPTION_LABEL': 'Acerca de Ti',
            'SECRECT_QUESTION_LABEL': 'Pregunta Secreta',
            'SECRECT_ANSWER_LABEL': 'Respuesta Secreta',
            'OLD_PASSWORD_LABEL': 'Viejo Contraceña',
            'NEW_PASSWORD_LABEL': 'Nueva Contraceña',
            'REPEAT_NEW_PASSWORD_LABEL': 'Repetir nueva Contraceña',
            'CHANGE_PASSWORD_LABEL': 'Cambiar Contraceña',
            'GROUPS_LABEL': 'Grupos',
            'GROUPS_PLURAL_LABEL': 'Grupos',
            'ADVIABLE_PERMISIONS_PLURAL_LABEL': 'Permisos Disponibles',
            'ADVIABLE_CHOSSEN_PLURAL_LABEL': 'Permisos Choosen',
            'COMMENTS_LABEL': 'Commentarios',
            'THEMES_LABEL': 'Plantillas',
            'SEO_LABEL': 'Seo',
            'META_TITLE_LABEL': 'Meta Titulo',
            'META_DESCRIPTION_LABEL': 'Meta Descripcion',
            'SLUG_LABEL': 'Slug',
            'CATEGORY_LABEL': 'Categoria',
            'CATEGORY_PLURAL_LABEL': 'Categories',
            'PUBLISH_LABEL':'Publicar',
            'USERNAME_LABEL':'Usuario',
            'DROP_FILES_LABEL':'Arastra los archios aqui y espera a que suban',
            'UNLOADED_FILES_LABEL':'Tus archivos no estan actualmente subidos', 
            'NAVIGATION_PLURAL_LABEL':'Navegacion',   
            'NAVIGATION_ITEMS_PLURAL_LABEL': 'Navigation Items', 
            'DRAG_ELEMENTS_LABEL':'Arrastra Elementos',
            'ON_FEED_LABEL':'Mostrar en el Feed?',
            'FEATURED_LABEL':'Destacado',
            'TAGS_LABEL':'Tags',
            'PAGES_LABEL':'Pagina',
            'PAGES_PLURAL_LABEL':'Paginas',
            'TAX_LABEL':'Impuesto',
            'TAXES_LABEL':'Impuestos',
            'ORDER_LABEL':'Orden de Compra',
            'ORDER_PLURAL_LABEL':'Ordenes de Compra',
            'DISCOUNT_LABEL':'Descuento',
            'DISCOUNT_PLURAL_LABEL':'Descuentos',
            'EXCERPT_LABEL':'Extracto',
            'MEDIA_ALBUM_PLURAL_LABEL':'Media Albums',
            'MEDIA_ALBUM_LABEL':'Media Album',
            'CITY_LABEL': "Ciudad",
            'COUNTRY_LABEL': "Pais",
            'PERCENT_LABEL': "Porcentaje",
      });
     
      $translateProvider.preferredLanguage('ES');
    }]);
});

