from ast import literal_eval

from odoo import fields, models, api
from odoo.exceptions import UserError


class PosSettings(models.TransientModel):
    _inherit = "res.config.settings"

    discount_limit = fields.Float(string="Discount Limit", related='pos_config_id.discount_limit', readonly=False,
                                  store=True)
    pos_category_ids = fields.Many2many("pos.category", 'catg_rel', 'catg_id', 'catg_us')

    def set_values(self):
        res = super(PosSettings, self).set_values()
        self.env['ir.config_parameter'].sudo(). \
            set_param('pos_discount_limit.pos_category_ids', self.pos_category_ids.ids)
        print('set', res)
        return res

    @api.model
    def get_values(self):
        res = super(PosSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        com_categories = with_user.get_param('pos_discount_limit.pos_category_ids')
        res.update(pos_category_ids=[(6, 0, literal_eval(com_categories))] if com_categories else False, )
        print('get', res)
        return res

    @api.constrains("discount_limit")
    def validate_disc(self):
        if self.discount_limit > 100:
            raise UserError("Enter a Value Upto 100")


class PosConfig(models.Model):
    _inherit = "pos.config"

    discount_limit = fields.Float()

    @api.model
    def get_category(self):
        res = self.env['ir.config_parameter'].sudo().get_param('pos_discount_limit.pos_category_ids')
        print("qwertyui", res)
        return eval(res)
