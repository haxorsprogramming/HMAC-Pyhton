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

document.querySelector('#txtUsername').focus();