// page/component/new-pages/user/address/address.js
Page({
  data:{
    address:{
      name:'',
      phone:'',
      detail:''
    }
  },
  onLoad(){
    var self = this;
    
    wx.getStorage({
      key: 'address',
      success: function(res){
        self.setData({
          address : res.data
        })
      }
    })
  },
  formSubmit(){  //缓存用户个人信息，并传送至后台保存
    var self = this;
    if(self.data.address.name && self.data.address.phone && self.data.address.detail){
      wx.setStorage({
        key: 'address',
        data: self.data.address,
        success(){
          wx.navigateBack();
        }
      }),
        console.log(self.data.address.name),
        wx.request({
          url: 'http://127.0.0.1:8000/addAddress/',
          method: 'post',
          data: {
            name: self.data.address.name, phone: self.data.address.phone, detail: self.data.address.detail,
            storage: wx.getStorageSync('storage') || []
          },
          header: {
            'content-type': 'application/x-www-form-urlencoded'
          },
          success: function (res) {
           console.log('666')
            
          }
        })    
    }else{
      wx.showModal({
        title:'提示',
        content:'请填写完整资料',
        showCancel:false
      })
    }
  },
  bindName(e){
    this.setData({
      'address.name' : e.detail.value
    })
  },
  bindPhone(e){
    this.setData({
      'address.phone' : e.detail.value
    })
  },
  bindDetail(e){
    this.setData({
      'address.detail' : e.detail.value
    })
  }
})