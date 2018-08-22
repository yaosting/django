// page/component/details/details.js
Page({
  data:{
    goods: {
    },
    num: 1,
    totalNum: 0,
    hasCarts: false,
    curIndex: 0,
    show: false,
    scaleCart: false
  },

  addCount() {
    let num = this.data.num;
    num++;
    this.setData({
      num : num
    })
  },

  addToCart() {
    const self = this;
    const num = this.data.num;
    let total = this.data.totalNum;
    let goods = this.data.goods;
    self.setData({
      show: true
    })
    setTimeout( function() {
      self.setData({
        show: false,
        scaleCart : true
      })
      setTimeout( function() {
        self.setData({
          scaleCart: false,
          hasCarts : true,
          totalNum: num + total
        })
      }, 200)
    }, 300)
    wx.request({
      url: 'http://127.0.0.1:8000/oneAddToCart/',
      method: 'post',
      data: {
        id: goods.id, title: goods.title, image: goods.image, num: num, price: goods.price, selected: true, nickname: wx.getStorageSync('nickname') || [], storage: wx.getStorageSync('storage') || []
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
      }
    })
  },

  bindTap(e) {
    const index = parseInt(e.currentTarget.dataset.index);
    this.setData({
      curIndex: index
    })
  },
  
  onShow:function(){
    var pages = getCurrentPages();
    var prevPage = pages[pages.length - 2];
    this.data.goods = prevPage.data.goods[0]
    // console.log(this.data.good1)
    this.setData({
      goods:this.data.goods
    })
  },

  onUnload: function () {
    wx.navigateBack({
      delta: 1
    })
  },


 
})