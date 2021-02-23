class RPY:
    to_card = {(False, False): "!", (False, True): "+", (True, False): "?", (True, True): "*"}
    from_card = {"!": (False, False), "+": (False, True), "?": (True, False), "*": (True, True)}

    symbol_unique = '-u'
    symbol_private = '-p'
    symbol_static = '-s'

    @classmethod
    def rpy_to_cfg(cls, rpy: str) -> dict:
        config = {}

        config["name"] = rpy[1:].split('[', 1)[0]
        config["type_"] = rpy.split('[', 1)[1].split(']', 1)[0]

        optional, multiple = cls.from_card[rpy[0]]

        if optional:
            config["optional"] = optional

        if multiple:
            config["multiple"] = multiple

        if cls.symbol_unique in rpy:
            config["unique"] = True

        if cls.symbol_private in rpy:
            config["private"] = True

        if cls.symbol_static in rpy:
            config["static"] = True

        return config

    @classmethod
    def cfg_to_rpy(cls, **config):
        card = cls.to_card[(config.get('optional', False), config.get('multiple', False))]

        u = f" {cls.symbol_unique}" if config.get('unique', False) else ""
        p = f" {cls.symbol_private}" if config.get('private', False) else ""
        s = f" {cls.symbol_static}" if config.get('static', False) else ""

        return card + config['name'] + "[" + config['type'] + "]" + u + p + s
