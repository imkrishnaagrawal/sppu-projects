var myApp = angular.module('app', ['angularFileUpload']);



myApp.controller('DownloadController', function ($scope, $http) {
    $scope.files = []
    //console.log("Hello");
    $http.get('/filenames').then(function (res) {
        console.log(res['data']);
        $scope.files = res['data'];

    });
    console.log($scope.files)
    $scope.deleteItem = function (file, index) {
        console.log(index);
        $http.get('/deleteFile/' + file).then(function (res) {
            console.log(res)
            if (res['data']['status'].toString() == "success") {
                $scope.files.splice(index, 1);
                console.log($scope.files);
            }
        });
    }
});

myApp.controller('AppController', ['$scope', 'FileUploader', function ($scope, FileUploader) {
    var uploader = $scope.uploader = new FileUploader({
        url: '/upload'
    });

    // FILTERS

    // a sync filter
    uploader.filters.push({
        name: 'syncFilter',
        fn: function (item /*{File|FileLikeObject}*/ , options) {
            console.log('syncFilter');
            return this.queue.length < 10;
        }
    });

    // an async filter
    uploader.filters.push({
        name: 'asyncFilter',
        fn: function (item /*{File|FileLikeObject}*/ , options, deferred) {
            console.log('asyncFilter');
            setTimeout(deferred.resolve, 1e3);
        }
    });

    // CALLBACKS

    uploader.onWhenAddingFileFailed = function (item /*{File|FileLikeObject}*/ , filter, options) {
        console.info('onWhenAddingFileFailed', item, filter, options);
    };
    uploader.onAfterAddingFile = function (fileItem) {
        console.info('onAfterAddingFile', fileItem);
    };
    uploader.onAfterAddingAll = function (addedFileItems) {
        console.info('onAfterAddingAll', addedFileItems);
    };
    uploader.onBeforeUploadItem = function (item) {
        console.info('onBeforeUploadItem', item);
    };
    uploader.onProgressItem = function (fileItem, progress) {
        console.info('onProgressItem', fileItem, progress);
    };
    uploader.onProgressAll = function (progress) {
        console.info('onProgressAll', progress);
    };
    uploader.onSuccessItem = function (fileItem, response, status, headers) {
        console.info('onSuccessItem', fileItem, response, status, headers);
    };
    uploader.onErrorItem = function (fileItem, response, status, headers) {
        console.info('onErrorItem', fileItem, response, status, headers);
    };
    uploader.onCancelItem = function (fileItem, response, status, headers) {
        console.info('onCancelItem', fileItem, response, status, headers);
    };
    uploader.onCompleteItem = function (fileItem, response, status, headers) {
        console.info('onCompleteItem', fileItem, response, status, headers);
    };
    uploader.onCompleteAll = function () {
        console.info('onCompleteAll');
    };

    //console.info('uploader', uploader);
}]);