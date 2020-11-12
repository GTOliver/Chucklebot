import random

OPERATION_TOKENS = ["+", "-"]


class CalculationException(Exception): pass


def get_response(input_message):
    value, instruction_str, evaluation_str = evaluate(input_message)
    if value is None:
        return "Well that's just not possible"
    else:
        msg = "Rolling: (" + instruction_str + ") = "
        str_val = str(value)
        if evaluation_str != str_val:
            msg += "`" +evaluation_str + "` = "
        msg += "**" + str_val + "**"
        return msg


def evaluate(expression):
    try:
        tokens = _parse(expression)
        tree = _tokens_to_tree(tokens)
        return tree.evaluate(), tree.instruction_string(), tree.evaluation_string()
    except CalculationException:
        return None, None, None


def _parse(expression):
    """ Parse an expression as a list of tokens """
    expression = ''.join(expression.split())

    tokens = []
    current_token = []

    def add_token(token_list):
        if len(token_list) != 0:
            tokens.append(''.join(token_list))

    for elem in expression:
        if elem in OPERATION_TOKENS:
            add_token(current_token)
            current_token = []
            add_token([elem])
        else:
            current_token.append(elem)
    add_token(current_token)
    return tokens


class LeafNode:
    def __init__(self, instruction):
        if not self._is_leaf_token(instruction):
            raise CalculationException()

        self._instruction = instruction
        self._evaluation = None
        self._eval_str = None

    def evaluate(self):
        if self._evaluation is None:
            self._evaluation, self._eval_str = self._evaluate_as_integer(self._instruction)
        return self._evaluation

    def instruction_string(self):
        return str(self._instruction)

    def evaluation_string(self):
        return self._eval_str

    @staticmethod
    def _evaluate_as_integer(token):
        try:
            return int(token), token
        except ValueError:
            results = token.split('d', 1)
            if len(results) == 2:
                n_dice = 1
                if results[0] != '':
                    n_dice = int(results[0])
                dice_val = int(results[1])
                accumulated = 0
                dice_rolls = []
                for _ in range(n_dice):
                    dice_roll = random.randint(1, dice_val)
                    dice_rolls.append(str(dice_roll))
                    accumulated += dice_roll
                dice_roll_str = '+'.join(dice_rolls)
                if n_dice != 1:
                    dice_roll_str = "(" + dice_roll_str + ")"
                return accumulated, dice_roll_str
        raise ValueError()

    @classmethod
    def _is_leaf_token(cls, token):
        try:
            cls._evaluate_as_integer(token)
            return True
        except ValueError:
            return False



class OperationNode:
    def __init__(self, token, lhs, rhs):
        if token not in OPERATION_TOKENS:
            raise CalculationException()
        self._token = token
        self._lhs = lhs
        self._rhs = rhs

    def evaluate(self):
        lhs = self._lhs.evaluate()
        rhs = self._rhs.evaluate()

        if self._token == "+":
            return lhs + rhs
        elif self._token == "-":
            return lhs - rhs
        else:
            return None

    def instruction_string(self):
        return self._lhs.instruction_string() + " " + self._token + " " + self._rhs.instruction_string()

    def evaluation_string(self):
        return self._lhs.evaluation_string() + " " + self._token + " " + self._rhs.evaluation_string()


def _tokens_to_tree(tokens):
    """ Convert tokens to a result string """

    if len(tokens) == 0:
        raise CalculationException()

    tree = LeafNode(tokens.pop(0))
    while len(tokens) > 0:
        operation_token = tokens.pop(0)
        if len(tokens) == 0:
            raise CalculationException()
        next_leaf = LeafNode(tokens.pop(0))

        new_tree = OperationNode(operation_token, tree, next_leaf)
        tree = new_tree
    return tree
