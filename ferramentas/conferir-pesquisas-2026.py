"""Segunda fonte de cada pesquisa de 2026: baixa a pagina citada (materia ou relatorio), guarda a captura e procura os numeros no texto.

Conferida = os dois numeros da Wikipedia (total) aparecem no texto da segunda fonte, ou os dois validos arredondados a uma casa.
Fonte alternativa: dados/derivados/pesquisas_2t_2026_fonte_alternativa.csv (instituto, campo_fim, url), quando a citada nao abre.
Saida: dados/derivados/pesquisas_2t_2026_conferencia.csv
"""
from __future__ import annotations

import hashlib
import html
import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from previsao.comum import BRUTOS, CAPTURAS, DERIV, registrar_arquivo, sha256  # noqa: E402

BRUTO_HTML = BRUTOS / "html-pesquisas-2026"  # fora do git

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}


def _texto_html(conteudo: bytes) -> str:
    t = conteudo.decode("utf-8", errors="ignore")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"[ 	]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


def texto_de(url: str) -> tuple[str, Path | None]:
    """Baixa a pagina uma vez. O HTML bruto fica fora do git (traz scripts e chaves de terceiros, como a chave publica do Google
    que o UOL poe nas paginas); no git fica so o texto extraido, que e o que a conferencia le."""
    nome = hashlib.sha1(url.encode()).hexdigest()[:16]
    txt = CAPTURAS / "pesquisas-2026" / f"{nome}.txt"
    pdf = CAPTURAS / "pesquisas-2026" / f"{nome}.pdf"
    bruto = BRUTO_HTML / f"{nome}.html"
    if pdf.exists():
        conteudo = pdf.read_bytes()
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(conteudo)) as doc:
                return " ".join((pg.extract_text() or "") for pg in doc.pages), pdf
        except Exception:
            return "", pdf
    if txt.exists():
        return txt.read_text(encoding="utf-8"), txt
    try:
        r = requests.get(url, headers=UA, timeout=40)
    except requests.RequestException:
        return "", None
    if r.status_code != 200 or len(r.content) < 2000:
        return "", None
    txt.parent.mkdir(parents=True, exist_ok=True)
    if url.lower().endswith(".pdf") or r.headers.get("content-type", "").startswith("application/pdf"):
        pdf.write_bytes(r.content)
        registrar_arquivo(pdf, url, "segunda fonte de pesquisa do 2o turno de 2026")
        return texto_de(url)
    BRUTO_HTML.mkdir(parents=True, exist_ok=True)
    bruto.write_bytes(r.content)
    txt.write_text(_texto_html(r.content), encoding="utf-8")
    registrar_arquivo(txt, url, f"texto extraido; HTML bruto (fora do git) sha256 {sha256(bruto)}")
    return txt.read_text(encoding="utf-8"), txt


def formas(x: float) -> list[str]:
    s = f"{x:.1f}".replace(".", ",")
    out = [s]
    if s.endswith(",0"):
        out.append(s[:-2])
    return out


def achou(texto: str, x: float) -> bool:
    return any(re.search(rf"(?<![\d,]){re.escape(f)}(?![\d])", texto) for f in formas(x))


def main() -> None:
    w = pd.read_csv(DERIV / "pesquisas_2t_2026_wikipedia.csv")
    alt_p = DERIV / "pesquisas_2t_2026_fonte_alternativa.csv"
    alt = pd.read_csv(alt_p) if alt_p.exists() else pd.DataFrame(columns=["instituto", "campo_fim", "url"])
    linhas = []
    for r in w.itertuples():
        urls = [r.url_wikipedia] + alt[(alt.instituto == r.instituto) & (alt.campo_fim == r.campo_fim)].url.tolist()
        res = {"instituto": r.instituto, "campo_fim": r.campo_fim, "conferida": False, "como": "", "url_conferida": "", "captura": ""}
        for u in urls:
            if not isinstance(u, str) or not u:
                continue
            t, cap = texto_de(u)
            if not t:
                continue
            fv = 100 * r.flavio_total / (r.flavio_total + r.lula_total)
            if achou(t, r.flavio_total) and achou(t, r.lula_total):
                res.update(conferida=True, como="totais no texto")
            else:
                # o valido publicado pode vir de totais com mais casas (Verita: 49,7 e 47,7 nos totais, 51,07 nos validos)
                for d in (0.0, 0.1, -0.1):
                    if achou(t, round(fv + d, 1)) and achou(t, round(100 - fv - d, 1)):
                        res.update(conferida=True, como=f"validos no texto (diferenca de arredondamento {d:+.1f})")
                        break
            if res["conferida"]:
                res.update(url_conferida=u, captura=str(cap.relative_to(CAPTURAS.parent.parent.parent)).replace("\\", "/") if cap else "")
                break
        linhas.append(res)
        print(r.instituto, r.campo_fim, res["conferida"], res["como"])
    out = DERIV / "pesquisas_2t_2026_conferencia.csv"
    pd.DataFrame(linhas).to_csv(out, index=False)
    registrar_arquivo(out, "ferramentas/conferir-pesquisas-2026.py")


if __name__ == "__main__":
    main()
