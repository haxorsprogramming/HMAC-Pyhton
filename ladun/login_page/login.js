var rToProses = server + 'login/proses';

var divLogin = new Vue({
    el : '#divLogin',
    data : {
        username : '',
        password : ''
    },
    methods : {
        loginAtc : function()
        {
            $.post(rToProses, function(data){
                console.log(data);
            })
        }
    }
});
$('#divImgAwal').hide();
document.querySelector('#txtUsername').focus();
// Webcam.set({
//     width: 320,
//     height: 240,
//     image_format:'jpeg',
//     jpeg_quality: 90
// });
// Webcam.attach('#my_camera');

// function take_snapshot() {
//     // take snapshot and get image data
//     Webcam.snap( function(data_uri) {
//         // display results in page
//         document.getElementById('results').innerHTML = 
//             '<h2>Here is your image:</h2>' + 
//             '<img src="'+data_uri+'"/>';
//     } );
// }
