// page/component/new-pages/cart/cart.js
Page({
  data: {
    carts:[],               // 购物车列表
    hasList:false,          // 列表是否有数据
    totalPrice:0,           // 总价，初始为0
    selectAllStatus:true,    // 全选状态，默认全选
    goods:[],
  },
  onShow() {
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:8000/test1/',
      method: 'post',
      data: {
         storage: wx.getStorageSync('storage') || []
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        // console.log(res.data);
        // console.log(typeof (res.data));
        that.setData({
          hasList: true,
          carts: res.data
        });
        that.getTotalPrice();
      },
      fail:function(){console.log("服务器忙，请稍后重试")}
      
    })
  },
  /**
   * 当前商品选中事件
   */
  selectList(e) {
    const index = e.currentTarget.dataset.index;
    let carts = this.data.carts;
    const selected = carts[index].selected;
    carts[index].selected = !selected;
    this.setData({
      carts: carts
    });
    this.getTotalPrice();
  },

  /**
   * 删除购物车当前商品
   */
  deleteList(e) {
    const index = e.currentTarget.dataset.index;
    let carts = this.data.carts;
    carts.splice(index,1);
    this.setData({
      carts: carts
      
    });
  
    if(!carts.length){
      this.setData({
        hasList: false
      });
    }else{
      this.getTotalPrice();
    }
  },

  /**
   * 购物车全选事件
   */
  selectAll(e) {
    let selectAllStatus = this.data.selectAllStatus;
    selectAllStatus = !selectAllStatus;
    let carts = this.data.carts;

    for (let i = 0; i < carts.length; i++) {
      carts[i].selected = selectAllStatus;
    }
    this.setData({
      selectAllStatus: selectAllStatus,
      carts: carts
    });
    this.getTotalPrice();
  },

  /**
   * 绑定加数量事件
   */
  addCount(e) {
    const index = e.currentTarget.dataset.index;
    let carts = this.data.carts;
    let num = carts[index].num;
    num = num + 1;
    carts[index].num = num;
    this.setData({
      carts: carts
    });
    this.getTotalPrice();
  },

  /**
   * 绑定减数量事件
   */
  minusCount(e) {
    const index = e.currentTarget.dataset.index;
    let carts = this.data.carts;
    let num = carts[index].num;
    if(num <= 1){
      return false;
    }
    num = num - 1;
    carts[index].num = num;
    this.setData({
      carts: carts
    });
    this.getTotalPrice();
  },

  /**
   * 计算总价
   */
  getTotalPrice() {
    let carts = this.data.carts;                  // 获取购物车列表
    let total = 0;
    for(let i = 0; i<carts.length; i++) {         // 循环列表得到每个数据
      if(carts[i].selected) {                     // 判断选中才会计算价格
        total += carts[i].num * carts[i].price;   // 所有价格加起来
      }
    }
    this.setData({                                // 最后赋值到data中渲染到页面
      carts: carts,
      totalPrice: total.toFixed(2)
    });
  },
  addCart: function (event){
    wx.navigateTo({
      url: '../orders/orders',
    })
   var that = this;
   that.setData({
     goods: that.data.carts
   })
   console.log(that.data.goods)
   
 }
  // 添加至数据库//
// addCart: function (event) {
  
//   var that = this;
//   let ca = JSON.stringify(this.data.carts);
//   console.log(ca);
//   console.log(typeof (this.data.carts))
//   console.log(typeof(ca));
//   wx.request({
//     url: 'http://127.0.0.1:8000/test/',
//     method:'post',
//     data :{
//       cart: ca, nickname: wx.getStorageSync('nickname') || [], storage: wx.getStorageSync('storage') || []
//     },
//     header:{
//       'content-type': 'application/x-www-form-urlencoded'
//     },
//     success:function(res){  
//       console.log(res.data)
//       wx.setStorageSync('ordernumber', res.data)
//     }
//   })
//   },
})
