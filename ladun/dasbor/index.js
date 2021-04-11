// vue object 
var divMenu = new Vue({
    delimiters: ["[[", "]]"],
    el : '#divMenu',
    data : {

    },
    methods : {
        berandaAtc : function()
        {
            divMain.titleApps = "Beranda";
            renderMenu("dashboard/beranda");
        },
        manajemenPegawai : function()
        {
            divMain.titleApps = "Manajemen Pegawai";
            renderMenu("dashboard/manajemen-pegawai");
        }
    }
});

var divMain = new Vue({
    delimiters: ["[[", "]]"],
    el : '#divMain',
    data : {
        titleApps : 'Beranda'
    },
    methods : {

    }
});


// inisialisasi & function 
divMenu.berandaAtc();

function renderMenu(halaman){
    progStart();
    $('#divUtama').html("Memuat halaman ..");
    $('#divUtama').load(server+halaman);
    progStop();
}

function progStart()
{
  NProgress.start();
}

function progStop()
{
  NProgress.done();
}