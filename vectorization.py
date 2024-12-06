import argparse
import os
from argparse import SUPPRESS, ArgumentParser

# from llama_index.agent.openai import OpenAIAgent, OpenAIAgentWorker
# from llama_index.core.agent import AgentRunner
# from core.models import ClipModel, MinillmModel
from core.models import MinillmModel
from service.pools.vectorization import VectorizationService


def build_argparser():
    """
    Build and return the argument parser.

    This function creates and configures an ArgumentParser for the script, including
    various command-line arguments that the user can provide.

    Returns:
        ArgumentParser: Configured ArgumentParser object.
    """

    def valid_path(path):
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(f"Invalid path: {path}")
        return path

    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group("Options")
    args.add_argument(
        "-h",
        "--help",
        action="help",
        default=SUPPRESS,
        help="Show this help message and exit.",
    )
    args.add_argument(
        "-d",
        "--data_folder",
        required=True,
        type=valid_path,
        help="The path of dataset. Must be a valid path.",
    )
    args.add_argument(
        "-t",
        "--table_name",
        default="rag_data",
        help="the table name to save vectorization data",
    )
    args.add_argument(
        "-tools",
        default="default",
        help="the rag method to create vectorization data , you can use 'ai' to get the best data.",
    )
    return parser


if __name__ == "__main__":
    args = build_argparser().parse_args()
    if len(os.sys.argv) == 1:
        args.print_help()
        os.sys.exit(1)
    data_folder = str(args.data_folder)
    table_name = str(args.table_name)
    tools = str(args.tools)

    text_emb_model = MinillmModel()
    # img_emb_model = ClipModel()

    # rag_service = VectorizationService(
    #     text_emb_model=text_emb_model, img_emb_model=img_emb_model, recreate=recreate
    # )
    rag_service = VectorizationService(
        text_emb_model=text_emb_model, table_name=table_name, tools=tools
    )
    rag_service.run(data_folder=data_folder)
    print(
        f"Success update vector db! data path:{data_folder} ,tools : {tools}, more message plz see logs!"
    )
