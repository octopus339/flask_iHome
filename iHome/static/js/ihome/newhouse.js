function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas',function (response) {
        if (response.errno == 0){
            $.each(response.data,function (i,area) {
                //渲染城区信息到页面
                // $('#area-id').append('<option value="'+area.aid+'">'+area.aname+'</option>')
                // 使用art-template模板引擎中的js生成要渲染的html内容
                var html = template('areas-tmpl',{'areas':response.data});
                // 将生成的html赋值给某个标签
                $('#area-id').html(html)

            })

        }else {
            alert(response.errmsg)
        }

    });



    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        event.preventDefault();
        var params={};
        // 收集$(this).serializeArray表单中的所有带有name的input标签数据
        //.map生成字典对象obj，封装到数组中,然后遍历每个字典
        //// obj == {name:'title',value:'1'}
        $(this).serializeArray().map(function (obj) {
            params[obj.name] = obj.value
        });
        console.log(params);

        // $.ajax({
        //     url:'',
        //     type:'post',
        //     data:JSON.stringify(params),
        //     contentType:'application/json',
        //     headers:{'X-CSRFToken':getCookie('csrf_token')},
        //     success:function (response) {
        //         if (response.errno == 0){
        //
        //         }else if (response.errno == '4101'){
        //             location.href = 'login.html'
        //         }
        //         else {
        //             alert(response.errmsg)
        //         }
        //
        //     }
        // })

    })

    // TODO: 处理图片表单的数据

})