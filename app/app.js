App({
  globalData: {
    nickName:'',
  },
  onLaunch:function(){
  
    /**
     * 获取用户信息
     */
    wx.login({
        success: function (res) {
          if (res.code){
            wx.request({
              url: 'http://127.0.0.1:8000/getid/', //接口地址
              method: 'post',
              data: { code: res.code, nickname: wx.getStorageSync('nickname') || [] },
              header: {
                'content-type': 'application/x-www-form-urlencoded' //默认值
              },
              success: function (res) {
                console.log(res.data) 
                wx.setStorageSync('storage', res.data)
                // wx.getStorage({
                //   key: 'storage',
                //   success: function (res) {
                //     console.log(res.data)
                //   }
                // })
            }
        })     
            wx.getUserInfo({
              success: function (res) {
                console.log(res.userInfo.nickName);
                wx.setStorageSync('nickname', res.userInfo.nickName)
                // var searchData = wx.getStorageSync('nickname') || []
              },
              fail: function () {
                console.log("启用app.getUserInfo函数，失败！");
              },
              });
          }
          else {
            console.log('获取用户登录态失败！' + res.errMsg)
          }
        },
      fail: function () {
        console.log("启用wx.login函数，失败！");
      },
    });
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
  },
  globalData: {
    hasLogin: false
  }
})
