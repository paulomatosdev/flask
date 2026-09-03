from unittest.mock import Mock, patch

import pytest
from src.utils import eleva_quadrado, requires_roles
from http import HTTPStatus



@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected

@pytest.mark.parametrize(
    "test_input,exc_class,msg", 
    [
        ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), 
        (None, TypeError, "")
    ]
)

def test_eleva_quadrado_falha(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)  # Passando uma string em vez de um número
    assert str(exc.value) == msg



def test_requires_roles_sucesso(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_roles("admin")(lambda: "Successo")
    result = decorated_function()
    assert result == "Successo"

def test_requires_roles_falha(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "user"

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_roles("admin")(lambda: "Successo")
    result = decorated_function()
    assert result == {"message": "Usuário não tem acesso."}, HTTPStatus.FORBIDDEN

    
    