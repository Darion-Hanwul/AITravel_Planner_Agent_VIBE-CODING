import asyncio
import sys

from app.config.settings import settings
from app.rag.pipeline import RagPipeline

def print_config() -> None:
    print("=" * 60)
    print(" BACKEND RAG STREAMING SANDBOX ")
    print("=" * 60)

    print("[i] Ollama URL   :", settings.OLLAMA_BASE_URL)
    print("[i] Ollama Model :", settings.OLLAMA_MODEL)

    print("=" * 60)

async def main() -> None:

    print_config()

    try:
        rag_pipeline = RagPipeline()

        print(
            "[✓] RagPipeline berhasil diinisialisasi."
        )

    except Exception as e:

        print(
            "\n[X] Gagal menginisialisasi RagPipeline."
        )

        print(
            f"Error Type   : {type(e).__name__}"
        )

        print(
            f"Error Detail : {str(e)}"
        )

        sys.exit(1)

    print(
        "\n"
        + "=" * 60
    )

    print(
        " LIVE STREAMING RAG TEST "
    )

    print(
        "=" * 60
    )

    print(
        "Ketik 'exit' atau 'keluar' untuk berhenti."
    )

    print()

    while True:

        try:

            query = input(
                "User -> "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print(
                "\n\nProgram dihentikan."
            )

            break

        if not query:

            continue

        if query.lower() in (
            "exit",
            "keluar",
        ):

            print(
                "\nProgram selesai."
            )

            break

        print(
            "\n"
            + "=" * 60
        )

        print(
            "🤖 AI Agent Response"
        )

        print(
            "=" * 60
        )

        full_response = []

        try:

            async for chunk in (
                rag_pipeline.execute_rag_stream(
                    query=query,
                )
            ):

                full_response.append(
                    chunk
                )

                print(
                    chunk,
                    end="",
                    flush=True,
                )

            print(
                "\n"
            )

            print(
                "-" * 60
            )

            print(
                "[✓] Streaming selesai."
            )

            print(
                "[i] Response length:",
                len(
                    "".join(
                        full_response
                    )
                ),
                "karakter",
            )

            print(
                "-" * 60
            )

        except Exception as e:

            print(
                "\n"
                + "=" * 60
            )

            print(
                "[X] Streaming RAG Error"
            )

            print(
                f"Error Type   : {type(e).__name__}"
            )

            print(
                f"Error Detail : {str(e)}"
            )

            print(
                "=" * 60
            )

        print()


if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print(
            "\n\nProgram dihentikan oleh user."
        )

    except Exception as e:

        print(
            "\n\n"
            "[FATAL ERROR]"
        )

        print(
            f"{type(e).__name__}: {str(e)}"
        )