Page({
  data: {
    imgUrls: [
      '/image/b1.jpg',
      '/image/b2.jpg',
      '/image/b3.jpg'
    ],
    indicatorDots: false,
    autoplay: false,
    interval: 3000,
    duration: 800,
    goods:{},
  },

oneToGood: function (event) {
  var that = this;
  var viewId = event.currentTarget.id;
  // var viewDataSet = event.currentTarget.dataset;
  // var viewText = viewDataSet.t;
  console.log(viewId)
    wx.request({
      url: 'http://127.0.0.1:8000/oneToGood/',
      method: 'post',
      data:{
        id:viewId,
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        that.setData({
          goods: res.data
        })
        console.log(that.data.goods)
        wx.navigateTo({
          url: 'details/details',
        })
      }
    })
  },





})