(function(window) {

    // Namespace our stuff
    if(window.ML === undefined) {
        window.ML = {};
    }
    var ML = window.ML;

    ////////////////////////////////////////////////////////////////////
    // Helpers
    //

    ML.isDefined = function(obj) {
        return typeof obj != 'undefined';
    };
    ML.isUndefined = function(obj) {
        return !ML.isDefined(obj);
    };
    ML.isEmpty = function(list) {
        return ML.isUndefined(list) || !list || (ML.isDefined(list.length) && list.length <= 0);
    };

    ML.log = function(msg) {
        if (window && window.console && window.console.log) {
            window.console.log(msg);
        }
    };

})(window);
