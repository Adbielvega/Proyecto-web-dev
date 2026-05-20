const API = "/api";

let loggedUser = null;

let currentSort = "recent";

function showMessage(text, type = "info") {

    const colors = {

        info: "bg-blue-50 text-blue-800 border border-blue-200",

        success: "bg-green-50 text-green-800 border border-green-200",

        error: "bg-red-50 text-red-800 border border-red-200"
    };

    $("#messageBox")
        .removeClass()
        .addClass(`mb-6 rounded-2xl p-4 text-sm ${colors[type]}`)
        .text(text)
        .removeClass("hidden");
}

function getFormData(formSelector) {

    const data = {};

    $(formSelector)
        .serializeArray()
        .forEach(item => {

            data[item.name] = item.value;

        });

    return data;
}

function updateAuthUI() {

    if (loggedUser) {

        $("#btnShowLogin, #btnShowRegister")
            .addClass("hidden");

        $("#btnLogout, #btnNewRecipe")
            .removeClass("hidden");

    } else {

        $("#btnShowLogin, #btnShowRegister")
            .removeClass("hidden");

        $("#btnLogout, #btnNewRecipe, #recipeFormSection")
            .addClass("hidden");
    }
}

$("#btnNewRecipe").on("click", function() {

    $("#recipeFormSection")
        .toggleClass("hidden");
});

$("#recipeForm").on("submit", function(e) {

    e.preventDefault();

    $.ajax({

        url: `${API}/recipes`,

        method: "POST",

        contentType: "application/json",

        data: JSON.stringify(
            getFormData("#recipeForm")
        ),

        success: res => {

            showMessage(
                res.message,
                "success"
            );

            $("#recipeForm")[0].reset();

            $("#recipeForm [name='id']").val("");

            $("#recipeFormSection")
                .addClass("hidden");

            loadRecipes();
        },

        error: xhr => {

            showMessage(
                xhr.responseJSON?.message ||
                "No se pudo crear receta.",
                "error"
            );
        }
    });
});

function recipeCard(recipe) {

    return `

    <article class="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 flex flex-col gap-4">

        <div class="flex justify-between items-start">

            <div>

                <h4 class="text-xl font-bold">
                    ${recipe.title}
                </h4>

                <p class="text-sm text-slate-500">
                    Por ${recipe.author_name}
                </p>

            </div>

            <span class="text-xs rounded-full bg-blue-50 text-blue-700 px-3 py-1">

                ${recipe.prep_minutes} min

            </span>

        </div>

        <p class="text-slate-600">

            ${recipe.description}

        </p>

        <div class="flex justify-between items-center pt-3 border-t border-slate-100">

            <span class="text-sm font-semibold">

                ${recipe.likes_count || 0} likes

            </span>

            <div class="flex gap-2 flex-wrap">

                <button
                    class="btn-secondary likeRecipe"
                    data-id="${recipe.id}">

                     Like

                </button>

                <button
                    class="btn-secondary favoriteRecipe"
                    data-id="${recipe.id}">

                    Favorita

                </button>

                <button
                    class="btn-secondary editRecipe"
                    data-id="${recipe.id}">
                    Editar

                    </button>

            </div>

        </div>

    </article>
    `;
}

function loadRecipes() {

    $.get(
        `${API}/recipes?sort=${currentSort}`,

        function(res) {

            const cards = res.data
                .map(recipeCard)
                .join("");

            $("#recipesGrid").html(
                cards ||
                `<p>No hay recetas.</p>`
            );
        }

    ).fail(() => {

        showMessage(
            "No se pudieron cargar recetas.",
            "error"
        );
    });
}

$(".sortBtn").on("click", function() {

    currentSort = $(this).data("sort");

    loadRecipes();
});

$(document).on("click", ".likeRecipe", function() {

    const id = $(this).data("id");

    $.ajax({

        url: `${API}/recipes/${id}/like`,

        method: "POST",

        success: res => {

            showMessage(
                res.message,
                "success"
            );

            loadRecipes();
        },

        error: xhr => {

            showMessage(
                xhr.responseJSON?.message ||
                "Debe iniciar sesion.",
                "error"
            );
        }
    });
});

$(document).on("click", ".favoriteRecipe", function() {

    const id = $(this).data("id");

    $.ajax({

        url: `${API}/recipes/${id}/favorite`,

        method: "POST",

        success: res => {

            showMessage(
                res.message,
                "success"
            );
        },

        error: xhr => {

            showMessage(
                xhr.responseJSON?.message ||
                "Debe iniciar sesion.",
                "error"
            );
        }
    });
});

$(document).on("click", ".editRecipe", function() {

    const card = $(this)
        .closest("article");

    const id = $(this).data("id");

    const title = card.find("h4").text().trim();

    const description = card
        .find("p.text-slate-600")
        .text()
        .trim();

    $("#recipeFormSection")
        .removeClass("hidden");

    $("#recipeForm [name='id']")
        .val(id);

    $("#recipeForm [name='title']")
        .val(title);

    $("#recipeForm [name='description']")
        .val(description);

    $("html, body").animate({
        scrollTop: $("#recipeFormSection").offset().top
    }, 500);
});

$("#btnShowLogin").on("click", () => {

    $("#loginForm")
        .toggleClass("hidden");

    $("#registerForm")
        .addClass("hidden");
});

$("#btnShowRegister").on("click", () => {

    $("#registerForm")
        .toggleClass("hidden");

    $("#loginForm")
        .addClass("hidden");
});

$("#registerForm").on("submit", function(e) {

    e.preventDefault();

    const data = getFormData("#recipeForm");

const id = data.id;

const method = id ? "PUT" : "POST";

const url = id
    ? `${API}/recipes/${id}`
    : `${API}/recipes`;

$.ajax({

    url: url,

    method: method,

    contentType: "application/json",

    data: JSON.stringify(data),

        success: res => {

            showMessage(
                res.message,
                "success"
            );
        },

        error: xhr => {

            showMessage(
                xhr.responseJSON?.message ||
                "Error registrando usuario",
                "error"
            );
        }
    });
});

$("#loginForm").on("submit", function(e) {

    e.preventDefault();

    $.ajax({

        url: `${API}/login`,

        method: "POST",

        contentType: "application/json",

        data: JSON.stringify(
            getFormData("#loginForm")
        ),

        success: res => {

            loggedUser = res.data;

            updateAuthUI();

            showMessage(
                `Bienvenido ${loggedUser.name}`,
                "success"
            );

            $("#loginForm")
                .addClass("hidden");
        },

        error: xhr => {

            showMessage(
                xhr.responseJSON?.message ||
                "Credenciales invalidas",
                "error"
            );
        }
    });
});

$("#btnLogout").on("click", function() {

    $.post(`${API}/logout`)
        .always(() => {

            loggedUser = null;

            updateAuthUI();

            showMessage(
                "Sesion cerrada.",
                "info"
            );
        });
});

$(document).ready(function() {

    updateAuthUI();

    loadRecipes();
});