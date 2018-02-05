


//----------------------
window.GUID = function () 
{
    //------------------
    var S4 = function () 
    {
        return(
                Math.floor(
                        Math.random() * 0x10000 /* 65536 */
                    ).toString(16)
            );
    };
    //------------------

    return "GUID-" +(
            S4() + S4() + "-" +
            S4() + "-" +
            S4() + "-" +
            S4() + "-" +
            S4() + S4() + S4()
        );
};
    //----------------------

    
window.string_to_slug = function (str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();
  
    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;~#";
    var to   = "aaaaeeeeiiiioooouuuunc--------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
}

     






     