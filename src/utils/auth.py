"""
Sistema de Autenticação
"""

import streamlit as st
from ..config.settings import PASSWORD


def check_password() -> bool:
    """
    Sistema de autenticação com senha.

    Returns:
        bool: True se autenticado
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h1>🔐 Acesso Restrito - Sistema DIMP</h1>
                <p style='color: #666; margin-top: 20px;'>
                    Dashboard de Inteligência de Meios de Pagamento<br>
                    Receita Estadual de Santa Catarina
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            senha_input = st.text_input(
                "Digite a senha:",
                type="password",
                key="pwd_input",
                placeholder="Senha de acesso"
            )

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                if st.button("🔓 Entrar", use_container_width=True, type="primary"):
                    if senha_input == PASSWORD:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta")

            with col_btn2:
                if st.button("ℹ️ Ajuda", use_container_width=True):
                    st.info("Entre em contato com o administrador do sistema para obter acesso.")

        st.markdown("""
            <div style='text-align: center; margin-top: 50px; color: #999; font-size: 0.9rem;'>
                <p>Sistema desenvolvido por Auditor Fiscal Tiago Severo</p>
                <p>Versão 2.0 | © 2025 Receita Estadual SC</p>
            </div>
        """, unsafe_allow_html=True)

        st.stop()

    return True


def logout():
    """Realiza logout do sistema."""
    st.session_state.authenticated = False
    st.rerun()


def is_authenticated() -> bool:
    """Verifica se usuário está autenticado."""
    return st.session_state.get('authenticated', False)
