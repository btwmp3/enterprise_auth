from typing import Any, Dict

class PolicyEngine:
    @staticmethod
    def evaluate_abac_rule(rules: Dict[str, Any], context: Dict[str, Any]) -> bool:
        for key, condition in rules.items():
            # Безопасный парсинг ключа entity.field
            if '.' not in key:
                return False
            
            entity, field = key.split('.', 1)
            
            # Проверяем явное наличие ключа, а не value is None
            entity_context = context.get(entity)
            if not isinstance(entity_context, dict) or field not in entity_context:
                return False

            actual_value = entity_context[field]

            # Набор ABAC-операторов
            if "eq" in condition and actual_value != condition["eq"]:
                return False
            if "neq" in condition and actual_value == condition["neq"]:
                return False
            if "lte" in condition and actual_value > condition["lte"]:
                return False
            if "gte" in condition and actual_value < condition["gte"]:
                return False
            if "lt" in condition and actual_value >= condition["lt"]:
                return False
            if "gt" in condition and actual_value <= condition["gt"]:
                return False
            if "in" in condition and actual_value not in condition["in"]:
                return False

        return True

    @classmethod
    def check_access(
        cls,
        user_permissions: list[str],
        required_permission: str,
        abac_policy: dict | None,
        context: dict
    ) -> bool:
        # 1. Проверка RBAC
        if required_permission not in user_permissions:
            return False

        # 2. Проверка ABAC
        if abac_policy and "rules" in abac_policy:
            rules = abac_policy.get("rules") or {}
            if rules and not cls.evaluate_abac_rule(rules, context):
                return False

        return True