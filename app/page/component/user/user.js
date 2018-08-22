// page/component/new-pages/user/user.js
const app = getApp()
Page({
  data:{
    thumb:'',
    nickname:'',
    orders:[],
    hasAddress:false,
    address:{},
    hiddenName: true,
    inputTxt:'',

    orderItems: [
      {
        typeId: 0,
        name: '待付款',
        url: 'bill',
        imageurl: '../../images/person/personal_shipped.jpg',
      },
      {
        typeId: 1,
        name: '待发货',
        url: 'bill',
        imageurl: '../../images/person/personal_shipped.jpg',
      },
      {
        typeId: 2,
        name: '待收货',
        url: 'bill',
        imageurl: '../../images/person/personal_shipped.jpg'
      },
      {
        typeId: 3,
        name: '待评价',
        url: 'bill',
        imageurl: '../../images/person/personal_shipped.jpg'
      }
    ], 
  },
  //邀请码弹出
  modalcnt: function () {
    var that = this
      wx.request({
    url: 'http://127.0.0.1:8000/GetNumber/',
    method:'post',
    data :{
      storage: wx.getStorageSync('storage') || []
    },
    header:{
      'content-type': 'application/x-www-form-urlencoded'
    },
    success:function(res){  
       wx.setStorageSync('invitenumber', res.data)
    }
  }),
    wx.showModal({
      title: '您的邀请码',
      content: JSON.stringify(wx.getStorageSync('invitenumber') || []),
      confirmText:'复制',
      cancelText:'关闭',
      success: function (res) {
        if (res.confirm) {
          wx.setClipboardData({
            data: wx.getStorageSync('invitenumber') || [],
            success: function (res) {
              wx.getClipboardData({
                success: function (res) {        
                }
              })
            }
          })                     
        } else if (res.cancel) {        
        }
      }
    })
  },

  showok: function () {
    wx.showToast({
      title: '逐步开放中',
      icon:'waiting',
      duration: 2000
    })
  },
MyOrder :function(){
  wx.navigateTo({
    url: '../mineorder/mineorder',
  })

},

  // 我的伙伴
  popup: function () {
    var OT = wx.getStorageSync('OpenTeam') || []
    console.log(OT)
    if (OT=='1'){console.log('已开通')}
    else{
      console.log('0000')
    }










    this.setData({
      hiddenName: !this.data.hiddenName
    })
   
  },
  cancel: function () {
    this.setData({
      hiddenName: !this.data.hiddenName,
      inputTxt: '',
    })

  },
// 输入并保存
  setValue: function(e){
    this.setData({
      inputTxt: e.detail.value//将input至与data中的inputValue绑定
    })
  },
  //确定按钮
  confirm: function () {
    this.setData({
      hiddenName: !this.data.hiddenName,
    })
    console.log(this.data.inputTxt)
    wx.request({
      url: 'http://127.0.0.1:8000/CheckNumber/',
      method: 'post',
      data: {
        storage: wx.getStorageSync('storage') || [], Number: this.data.inputTxt ,
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        wx.setStorageSync('checktitle', res.data)
      }
    }),
    wx.showToast({
      title: JSON.stringify(wx.getStorageSync('checktitle') || []),
      icon:'warn',
      duration: 2000
    })
  },





  onLoad(){
    var self = this;
    /**
     * 获取用户信息
     */
    wx.getUserInfo({
      success: function(res){
        self.setData({
          thumb: res.userInfo.avatarUrl,
          nickname: res.userInfo.nickName
        })
      }
    }),

    /**
     * 发起请求获取订单列表信息
     */
    wx.request({
      url: 'http://www.gdfengshuo.com/api/wx/orders.txt',
      success(res){
        self.setData({
          orders: res.data.orders
        })
      }
    })
  },
  onShow(){
    var self = this;
    /**
     * 获取本地缓存 地址信息
     */
    wx.getStorage({
      key: 'address',
      success: function(res){
        self.setData({
          hasAddress: true,
          address: res.data
        })
      }
    })

    wx.request({
      url: 'http://127.0.0.1:8000/OpenTeam/',
      method: 'post',
      data: {
        storage: wx.getStorageSync('storage') || [],
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        wx.setStorageSync('OpenTeam', res.data)
      }
    })



  },
  /**
   * 发起支付请求
   */
  payOrders(){
    wx.requestPayment({
      timeStamp: 'String1',
      nonceStr: 'String2',
      package: 'String3',
      signType: 'MD5',
      paySign: 'String4',
      success: function(res){
        console.log(res)
      },
      fail: function(res) {
        wx.showModal({
          title:'支付提示',
          content:'<text>',
          showCancel: false
        })
      }
    })
  }
})