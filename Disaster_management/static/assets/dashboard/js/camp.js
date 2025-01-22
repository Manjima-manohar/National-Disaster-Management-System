<script>
document.getElementById('state').addEventListener('change', function() {
    var state = this.value;
    var campSelect = document.getElementById('camp_name');

    // Fetch camps based on state
    fetch(`/get-camps/?state=${state}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing options
            campSelect.innerHTML = '<option disabled selected>Select camp</option>';
            data.camps.forEach(camp => {
                var option = document.createElement('option');
                option.value = camp.id;
                option.textContent = camp.camp_name;
                campSelect.appendChild(option);
            });
        });
});
</script>
