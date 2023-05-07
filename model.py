import itertools
from transformers import CLIPTokenizer, CLIPTextModel
from diffusers.pipelines.stable_diffusion import StableDiffusionSafetyChecker
from diffusers import AutoencoderKL, DDPMScheduler, PNDMScheduler, StableDiffusionPipeline, UNet2DConditionModel


def load_tokenizer(pretrained_model_path, placeholder_token):
    tokenizer = CLIPTokenizer.from_pretrained(
        pretrained_model_path, subfolder="tokenizer")
    return tokenizer


def get_initializer_and_placeholder_ids(tokenizer, initializer_token, placeholder_token):
    token_ids = tokenizer.encode(initializer_token, add_special_tokens=False)
    if len(token_ids) > 1:
        raise ValueError("The initializer token must be a single token.")

    initializer_token_id = token_ids[0]
    placeholder_token_id = tokenizer.convert_tokens_to_ids(placeholder_token)
    return initializer_token_id, placeholder_token_id


def load_models(pretrained_model_path, tokenizer):
    text_encoder = CLIPTextModel.from_pretrained(
        pretrained_model_path, subfolder="text_encoder")
    vae = AutoencoderKL.from_pretrained(pretrained_model_path, subfolder="vae")
    unet = UNet2DConditionModel.from_pretrained(
        pretrained_model_path, subfolder="unet")

    text_encoder.resize_token_embeddings(len(tokenizer))
    return text_encoder, vae, unet


def freeze_params(params):
    for param in params:
        param.requires_grad = False


def setup_model(text_encoder, vae, unet, initializer_token_id, placeholder_token_id):
    token_embeds = text_encoder.get_input_embeddings().weight.data
    token_embeds[placeholder_token_id] = token_embeds[initializer_token_id]

    freeze_params(vae.parameters())
    freeze_params(unet.parameters())

    params_to_freeze = itertools.chain(
        text_encoder.text_model.encoder.parameters(),
        text_encoder.text_model.final_layer_norm.parameters(),
        text_encoder.text_model.embeddings.position_embedding.parameters(),
    )
    freeze_params(params_to_freeze)


pretrained_model_name_or_path = "sd-concept-output-carpet"
initializer_token = "carpet"
placeholder_token = "<moroccan-carpet>"

tokenizer = load_tokenizer(pretrained_model_name_or_path, placeholder_token)
initializer_token_id, placeholder_token_id = get_initializer_and_placeholder_ids(
    tokenizer, initializer_token, placeholder_token)
text_encoder, vae, unet = load_models(pretrained_model_name_or_path, tokenizer)
setup_model(text_encoder, vae, unet,
                     initializer_token_id, placeholder_token_id)

pipe = StableDiffusionPipeline.from_pretrained(
    pretrained_model_name_or_path)

