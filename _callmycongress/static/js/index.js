$('#member-search-form').submit(function(e) {
    console.log('Submitted member search form');
    e.preventDefault();

    const address = $(this).children('#address').val();
    console.log(`Address: ${address}`);
    const roles = $(this).children('#roles').val();
    console.log(`Roles: ${roles}`);

    const url = $(this).attr('action');
    console.log(`URL: ${url}`);

    $.ajax({
        url: url,
        type: 'GET',
        data: {
            'address': address,
            'roles': roles
        },
        success: function(response) {
            console.log('Successfully searched for my members!');
            console.log(response);
            for (var object in response) {
                createMember(response[object]);
            }
        },
        error: function(xhr, error, status) {
            console.log(`Error: ${error}, Status: ${status}`);
        }
    });
})

function createMember(object) {
    var container = $('#results');
    for (var key in object) {
        console.log(key, object[key]);
    };
    container.append(`
        <div class="card member">
            <a href="">${object.name}</a>

            <div class="card-body">
                <p class="card-text">Party: ${object.party}</p>
                <p class="card-text">Phone #: ${object.phones}</p>
                <p class="card-text">Website: ${object.urls}</p>
            </div>
        </div>
    `)
};