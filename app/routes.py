from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    current_app,
)
from app.models import Creator, Model, ModelVersion, File, Image, Tag
from app import db
from flask_paginate import Pagination, get_page_parameter
import os

main = Blueprint("main", __name__)


@main.route("/")
def index():
    # Get NSFW filter parameter
    nsfw = request.args.get("nsfw", "false")

    # Base query with NSFW filtering
    random_models_query = Model.query

    # Apply NSFW filter if needed
    if nsfw == "false":
        random_models_query = random_models_query.filter(Model.nsfw == False)

    # Get random models with their base models
    # We need to join with ModelVersion to get the base model info
    random_models = random_models_query.order_by(db.func.random()).limit(10).all()

    # Pre-fetch model versions for each model to avoid N+1 query problems
    for model in random_models:
        # Make sure each model has at least the first version loaded
        if model.versions.count() > 0:
            model.first_version = model.versions.first()
        else:
            model.first_version = None

    # Get random images for the banner (filtered for NSFW)
    # We need to be more explicit with our joining and filtering to ensure NSFW models don't show up
    if nsfw == "false":
        # This query ensures that we properly join and filter NSFW content
        featured_images = (
            db.session.query(Image)
            .join(ModelVersion, Image.model_version_id == ModelVersion.id)
            .join(Model, ModelVersion.model_id == Model.id)
            .filter(Model.nsfw == False)
            .order_by(db.func.random())
            .limit(5)
            .all()
        )
    else:
        # If NSFW is allowed, just get random images
        featured_images = Image.query.order_by(db.func.random()).limit(5).all()

    # Get all model types for quick filters
    model_types = db.session.query(Model.type).distinct().all()
    model_types = [t[0] for t in model_types if t[0]]

    # Get all base models for filter dropdown
    base_models = db.session.query(ModelVersion.base_model).distinct().all()
    base_models = [m[0] for m in base_models if m[0]]

    return render_template(
        "index.html",
        random_models=random_models,
        featured_images=featured_images,
        model_types=model_types,
        base_models=base_models,
        current_nsfw=nsfw,
    )


@main.route("/models")
def models():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["MODELS_PER_PAGE"]

    # Base query
    query = Model.query

    # Filter options
    type_filter = request.args.get("type")
    base_model_filter = request.args.get("base_model")
    sort_by = request.args.get("sort", "newest")
    nsfw = request.args.get("nsfw", "false")
    tags = request.args.getlist("tags")

    # Apply filters
    if type_filter:
        query = query.filter(Model.type == type_filter)

    # Apply base model filter
    if base_model_filter:
        query = query.join(ModelVersion).filter(
            ModelVersion.base_model == base_model_filter
        )

    if nsfw == "false":
        query = query.filter(Model.nsfw == False)

    if tags:
        for tag in tags:
            query = query.join(Tag, Model.id == Tag.model_id).filter(Tag.tag == tag)

    # Apply sorting
    if sort_by == "newest":
        query = query.order_by(Model.id.desc())
    elif sort_by == "downloads":
        query = query.order_by(Model.download_count.desc())

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    models = pagination.items

    # Get all model types for filter dropdown
    model_types = db.session.query(Model.type).distinct().all()
    model_types = [t[0] for t in model_types if t[0]]

    # Get all base models for filter dropdown
    base_models = db.session.query(ModelVersion.base_model).distinct().all()
    base_models = [m[0] for m in base_models if m[0]]

    # Get popular tags
    popular_tags = (
        db.session.query(Tag.tag, db.func.count(Tag.id).label("count"))
        .group_by(Tag.tag)
        .order_by(db.text("count DESC"))
        .limit(20)
        .all()
    )

    return render_template(
        "models.html",
        models=models,
        pagination=pagination,
        model_types=model_types,
        base_models=base_models,
        popular_tags=popular_tags,
        current_filters={
            "type": type_filter,
            "base_model": base_model_filter,
            "sort": sort_by,
            "nsfw": nsfw,
            "tags": tags,
        },
    )


@main.route("/models/<int:model_id>")
def model_detail(model_id):
    model = Model.query.get_or_404(model_id)
    versions = (
        ModelVersion.query.filter_by(model_id=model_id)
        .order_by(ModelVersion.index_in_model.desc())
        .all()
    )

    # Get preview images
    preview_images = []
    for version in versions:
        images = Image.query.filter_by(model_version_id=version.id).limit(4).all()
        preview_images.extend(images)

    # Get model tags
    tags = Tag.query.filter_by(model_id=model_id).all()

    # Get similar models (models with same tags)
    tag_ids = [tag.tag for tag in tags]
    similar_models = (
        Model.query.join(Tag, Model.id == Tag.model_id)
        .filter(Model.id != model_id)
        .filter(Tag.tag.in_(tag_ids))
        .group_by(Model.id)
        .order_by(db.func.count(Tag.id).desc())
        .limit(6)
        .all()
    )

    # Get all model types for related models section
    model_types = db.session.query(Model.type).distinct().all()
    model_types = [t[0] for t in model_types if t[0]]

    # Get related models by type
    related_by_type = (
        Model.query.filter(Model.type == model.type)
        .filter(Model.id != model.id)
        .order_by(db.func.random())
        .limit(4)
        .all()
    )

    return render_template(
        "model_detail.html",
        model=model,
        versions=versions,
        preview_images=preview_images,
        tags=tags,
        similar_models=similar_models,
        related_by_type=related_by_type,
        model_types=model_types,
    )


@main.route("/creators")
def creators():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["CREATORS_PER_PAGE"]

    # Base query
    query = Creator.query

    # Sort options
    sort_by = request.args.get("sort", "models")

    # Apply sorting
    if sort_by == "models":
        query = (
            query.outerjoin(Model, Creator.id == Model.creator_id)
            .group_by(Creator.id)
            .order_by(db.func.count(Model.id).desc())
        )
    elif sort_by == "downloads":
        query = (
            query.outerjoin(Model, Creator.id == Model.creator_id)
            .group_by(Creator.id)
            .order_by(db.func.sum(Model.download_count).desc())
        )
    elif sort_by == "name":
        query = query.order_by(Creator.username)

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    creators = pagination.items

    # Get all model types for related navigation
    model_types = db.session.query(Model.type).distinct().all()
    model_types = [t[0] for t in model_types if t[0]]

    return render_template(
        "creators.html",
        creators=creators,
        pagination=pagination,
        current_sort=sort_by,
        model_types=model_types,
    )


@main.route("/creators/<int:creator_id>")
def creator_detail(creator_id):
    creator = Creator.query.get_or_404(creator_id)

    # Get creator's models
    models = (
        Model.query.filter_by(creator_id=creator_id).order_by(Model.id.desc()).all()
    )

    # Calculate statistics
    model_count = len(models)
    download_count = sum(model.download_count for model in models)

    # Get all model types
    model_types = db.session.query(Model.type).distinct().all()
    model_types = [t[0] for t in model_types if t[0]]

    return render_template(
        "creator_detail.html",
        creator=creator,
        models=models,
        model_count=model_count,
        download_count=download_count,
        model_types=model_types,
    )


@main.route("/search")
def search():
    query = request.args.get("q", "")
    base_model_filter = request.args.get("base_model", "")
    nsfw = request.args.get("nsfw", "false")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["MODELS_PER_PAGE"]

    if not query:
        return redirect(url_for("main.index"))

    # Search models
    model_results = Model.query.filter(
        db.or_(Model.name.ilike(f"%{query}%"), Model.description.ilike(f"%{query}%"))
    )

    # Search creators
    creator_results = Creator.query.filter(Creator.username.ilike(f"%{query}%"))

    # Search tags
    tag_results = Tag.query.filter(Tag.tag.ilike(f"%{query}%"))

    # Get models from tag results
    tag_model_ids = [tag.model_id for tag in tag_results.all()]
    tag_models = Model.query.filter(Model.id.in_(tag_model_ids))

    # Combine model results
    combined_models = model_results.union(tag_models)

    # Apply base model filter if provided
    if base_model_filter:
        combined_models = combined_models.join(
            ModelVersion, Model.id == ModelVersion.model_id
        ).filter(ModelVersion.base_model == base_model_filter)

    # Apply NSFW filter
    if nsfw == "false":
        combined_models = combined_models.filter(Model.nsfw == False)

    # Pagination for models
    model_pagination = combined_models.paginate(
        page=page, per_page=per_page, error_out=False
    )
    models = model_pagination.items

    # Pagination for creators (simplified)
    creators = creator_results.limit(5).all()

    # Get all base models for filter dropdown
    base_models = db.session.query(ModelVersion.base_model).distinct().all()
    base_models = [m[0] for m in base_models if m[0]]

    # Get all model types for related navigation
    model_types = db.session.query(Model.type).distinct().all()
    model_types = [t[0] for t in model_types if t[0]]

    return render_template(
        "search.html",
        query=query,
        models=models,
        model_pagination=model_pagination,
        creators=creators,
        base_models=base_models,
        model_types=model_types,
        current_base_model=base_model_filter,
        current_nsfw=nsfw,
    )
