from abc import ABC, abstractmethod
import stmt
import expr


class Visitor:
    class Visitor(ABC):
        # @abstractmethod
        # def visit_assign_expr(self, expr: expr.Assign):
        #     pass

        @abstractmethod
        def visit_binary_expr(self, expr: expr.Binary):
            pass

        # @abstractmethod
        # def visit_conditional_expr(self, expr: Conditional):
        #     pass

        @abstractmethod
        def visit_grouping_expr(self, expr: expr.Grouping):
            pass

        @abstractmethod
        def visit_literal_expr(self, expr: expr.Literal):
            pass

        # @abstractmethod
        # def visit_logical_expr(self, expr: expr.Logical):
        #     pass

        @abstractmethod
        def visit_unary_expr(self, expr: expr.Unary):
            pass

        # @abstractmethod
        # def visit_variable_expr(self, expr: expr.Variable):
        #     pass

        # @abstractmethod
        # def visit_function_expr(self, expr: expr.Function):
        #     pass

        # @abstractmethod
        # def visit_call_expr(self, expr: expr.Call):
        #     pass

        # @abstractmethod
        # def visit_get_expr(self, expr: Get):
        #     pass

        # @abstractmethod
        # def visit_set_expr(self, expr: Set):
        #     pass

        # @abstractmethod
        # def visit_this_expr(self, expr: This):
        #     pass

        # @abstractmethod
        # def visit_super_expr(self, expr: Super):
        #     pass

        @abstractmethod
        def visit_expression_stmt(self, stmt: stmt.Expression):
            pass

        @abstractmethod
        def visit_print_stmt(self, stmt: stmt.Print):
            pass

        @abstractmethod
        def visit_var_stmt(self, stmt: stmt.Var):
            pass

        # @abstractmethod
        # def visit_block_stmt(self, stmt: Block):
        #     pass
        #
        # @abstractmethod
        # def visit_if_stmt(self, stmt: If):
        #     pass
        #
        # @abstractmethod
        # def visit_fun_stmt(self, stmt: Fun):
        #     pass
        #
        # @abstractmethod
        # def visit_return_stmt(self, stmt: Return):
        #     pass
        #
        # @abstractmethod
        # def visit_class_stmt(self, stmt: Class):
        #     pass
        #
        # @abstractmethod
        # def visit_while_stmt(self, stmt: While):
        #     pass
        #
        # @abstractmethod
        # def visit_break_stmt(self, stmt: Break):
        #     pass
