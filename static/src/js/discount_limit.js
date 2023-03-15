odoo.define('pos_discount_limit.Pos',function(require){
'use strict';
const ProductScreen =require('point_of_sale.ProductScreen');
const Registries=require('point_of_sale.Registries');
var rpc=require('web.rpc');
const discount_limit = (ProductScreen)=>class extends ProductScreen{
async _onClickPay() {

    var self=this;
    var category_values=0;
    var discount_value=this.env.pos.config.discount_limit
    console.log(discount_value,"seetings disc")
    await rpc.query({
    model:'pos.config',
    method:'get_category',
    args:[]
    }).then(function(result){
        category_values=result
        console.log(category_values,"settings cat")
    });

    var flag=0
    var list=[]
    $.each(this.env.pos.selectedOrder.orderlines,function(index,name){
    console.log(name.discount,"product_disc")
    console.log(name.product.pos_categ_id[0],"product cat")
    if (category_values.includes(name.product.pos_categ_id[0])){
        if(name.discount>discount_value){
         flag=1
         list.push(name.product.pos_categ_id[1])
        }
    }
    })

    if (flag==1){
    self.showPopup('ErrorPopup',{
            title:"Discount is not valid",
            body:"please enter  discount less than "+ discount_value + "% for product category " + list[0]
            });
    }else{
     super._onClickPay()
    }



}}
Registries.Component.extend(ProductScreen,discount_limit);
return ProductScreen;

});