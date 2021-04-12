var rToProses = server + "login/proses";
var rToDashboard = server + "main_app/beranda";
var step_verif = 0;

var divLogin = new Vue({
    el : '#divLogin',
    delimiters: ["[[", "]]"],
    data : {
        username : '',
        password : '',
        statusVerifikasi : 0,
        capVerifikasi : '',
        nama_pegawai : ''
    },
    methods : {
        loginAtc : function()
        {
            let username = document.querySelector('#txtUsername').value;
            let password = document.querySelector('#txtPassword').value;
            let ds = {'username':username, 'password':password}

            if(username === '' || password === ''){
                pesanUmumApp('warning', 'Isi field', 'Harap isi username & password!!!');
            }else{
                $.post(rToProses, ds, function(data){
                    console.log(data);
                    divLogin.nama_pegawai = data.nama_pegawai;
                    let status_login = data.status_login;
                    if(status_login === 'no_user'){
                        pesanUmumApp('warning', 'No user', 'Username tidak terdaftar!!!');
                    }else{
                        if(status_login === 'wrong_password'){
                            pesanUmumApp('warning', 'Isi field', 'Username & Password salah!!!');
                        }else{
                            $('#btnLoginAwal').hide();
                            $('#imgFotoSamping').hide();
                            $('#video').show();
                            loadWebcam();
                        }
                    }
                });
            }
        },
        captureAtc : function()
        {
            // let dataImg = document.querySelector("#imgHasil").getAttribute("src");
            var canvas = document.getElementById("cImg");
            var video = document.getElementById("video");
            canvas.getContext('2d').drawImage(video, 0, 0);
            console.log("loss");
        }
    }
});

$('#divImgAwal').hide();
document.querySelector('#txtUsername').focus();

function loadWebcam()
{
    const video = document.getElementById('video')

    Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('ladun/login_page/models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('ladun/login_page/models'),
    faceapi.nets.faceRecognitionNet.loadFromUri('ladun/login_page/models'),
    faceapi.nets.faceExpressionNet.loadFromUri('ladun/login_page/models')
    ]).then(startVideo)

    function startVideo() {
    navigator.getUserMedia(
        { video: {} },
        stream => video.srcObject = stream,
        err => console.error(err)
    )
    }

    video.addEventListener('play', () => {
    const canvas = faceapi.createCanvasFromMedia(video)
    document.body.append(canvas)
    const displaySize = { width: video.width, height: video.height }
    faceapi.matchDimensions(canvas, displaySize)
    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
        const resizedDetections = faceapi.resizeResults(detections, displaySize)
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
        faceapi.draw.drawDetections(canvas, resizedDetections)
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
    }, 100)
    })
}


function verifikasi_wajah()
{
    setTimeout(function(){
        divLogin.capVerifikasi = "Wajah terdeteksi, menunggu verifikasi ...";
    }, 4000);
    sukses_verifikasi();
}


function sukses_verifikasi()
{
    let nama_pegawai = divLogin.nama_pegawai;
    setTimeout(function(){
        pesanUmumApp('success', 'Sukses', 'Operator sukses terdeteksi : '+nama_pegawai);
        divLogin.capVerifikasi = "Berhasil ... mengarahkan ke halaman utama aplikasi ... ";
    }, 8000);
}

function pesanUmumApp(icon, title, text)
{
  Swal.fire({
    icon : icon,
    title : title,
    text : text
  });
}