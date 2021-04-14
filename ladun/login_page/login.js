var rToProses = server + "login/proses";
var rToDashboard = server + "main_app/beranda";
var rToIdentifikasiWajah = server + "login/identifikasi-wajah";
var rToGetDataPegawai = server + "login/get-data-pegawai";

var step_verif = 0;
var kdLogin = "";
var user_login = "";

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
                    let username = data.username;
                    user_login = username;
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
            var canvas = document.getElementById("cImg");
            var video = document.getElementById("video");
            canvas.getContext('2d').drawImage(video, 0, 0);
            let hasil = canvas.toDataURL();
            let ds = { 'hasil':hasil }
            $.post(rToIdentifikasiWajah, ds, function(data){
                let obj = JSON.parse(data.hasil);
                console.log(obj);
                let hasil_identifikasi = obj[0];
                let id_pegawai = hasil_identifikasi['id'];
                let nama = hasil_identifikasi['name'];
                let probabilitas = hasil_identifikasi['probability'];
                let ds = {'username':nama}
                if(nama === user_login){
                    $.post(rToGetDataPegawai, ds, function(data){
                        let nama = data.nama;
                        pesanUmumApp('success', 'Sukses', 'Berhasil mendeteksi user, nama pegawai yang sedang login adalah : '+ nama + ', Anda akan dialihkan ke halaman aplikasi dalam 3 detik');
                        
                        setTimeout(function(){
                            window.location.assign(server + 'main_app/beranda');
                        }, 4000);
                    });
                }else{
                    pesanUmumApp('warning', 'Failed', 'Gagal mendeteksi, wajah tidak cocok dengan database');
                    setTimeout(function(){
                        window.location.assign(server);
                    }, 2000);
                    
                }
                
            });
            
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
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
        const resizedDetections = faceapi.resizeResults(detections, displaySize);
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
        faceapi.draw.drawDetections(canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
        console.log("Mulai detect");
        step_verif++;
        if(step_verif === 20){
            divLogin.captureAtc();
        }
    }, 100);
    });
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