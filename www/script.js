// MOD: This event listener will now correctly start the animation by itself.
window.addEventListener("load", canvasApp, false);

function canvasApp() {
	if (!document.createElement('canvas').getContext) {
		return;
	}

	const theCanvas = document.getElementById("canvasOne");
    // Add a check to ensure the canvas element exists before proceeding
	if (!theCanvas) {
        console.error("Canvas element with ID 'canvasOne' not found.");
        return;
    }
	const context = theCanvas.getContext("2d");

	const displayWidth = theCanvas.width;
	const displayHeight = theCanvas.height;
	const fLen = 320; 
	const particleRad = 1.8;
	const sphereRad = 140;
	let turnSpeed = 2 * Math.PI / 1200;
	let turnAngle = 0;
	
	const particleList = {};
	const recycleBin = {};
	const numToAddEachFrame = 8;
	
	const sphereCenterZ = -3 - sphereRad;
	const projCenterX = displayWidth / 2;
	const projCenterY = displayHeight / 2;
	
	const rgbString = "rgba(0, 72, 255,";

	function addParticle(x0, y0, z0, vx0, vy0, vz0) {
		let newParticle;
        // Simplified particle recycling logic
		if (recycleBin.first) {
			newParticle = recycleBin.first;
			recycleBin.first = newParticle.next;
		} else {
			newParticle = {};
		}
		
        newParticle.next = particleList.first;
		if(particleList.first) particleList.first.prev = newParticle;
		particleList.first = newParticle;
		newParticle.prev = null;

		newParticle.x = x0;
		newParticle.y = y0;
		newParticle.z = z0;
		newParticle.velX = vx0;
		newParticle.velY = vy0;
		newParticle.velZ = vz0;
		newParticle.age = 0;
		newParticle.dead = false;
        p.stuckTime = 80 + Math.random() * 20;
		
		return newParticle;
	}

	function onTimer() {
		for (let i = 0; i < numToAddEachFrame; i++) {
			const theta = Math.random() * 2 * Math.PI;
			const phi = Math.acos(Math.random() * 2 - 1);
			const x0 = sphereRad * Math.sin(phi) * Math.cos(theta);
			const y0 = sphereRad * Math.sin(phi) * Math.sin(theta);
			const z0 = sphereRad * Math.cos(phi);
			addParticle(x0, 0 + y0, sphereCenterZ + z0, 0.002 * x0, 0.002 * y0, 0.002 * z0);
		}

		turnAngle = (turnAngle + turnSpeed) % (2 * Math.PI);
		const sinAngle = Math.sin(turnAngle);
		const cosAngle = Math.cos(turnAngle);

		context.fillStyle = "#000000";
		context.fillRect(0, 0, displayWidth, displayHeight);

		let p = particleList.first;
		while (p) {
			const nextParticle = p.next;
			p.age++;
			if (p.age > p.stuckTime) {
				p.x += p.velX;
				p.y += p.velY;
				p.z += p.velZ;
			}
			const rotX = cosAngle * p.x + sinAngle * (p.z - sphereCenterZ);
			const rotZ = -sinAngle * p.x + cosAngle * (p.z - sphereCenterZ) + sphereCenterZ;
			const m = 320 / (320 - rotZ);
			p.projX = rotX * m + projCenterX;
			p.projY = p.y * m + projCenterY;

			if (p.age > 200) p.dead = true;

			if (p.dead) {
				if(p.prev) p.prev.next = p.next;
                if(p.next) p.next.prev = p.prev;
                if(p === particleList.first) particleList.first = p.next;
                
                p.next = recycleBin.first;
                recycleBin.first = p;
			} else {
				const depthAlphaFactor = (1 - rotZ / -750);
				context.fillStyle = rgbString + Math.min(1, depthAlphaFactor) + ")";
				context.beginPath();
				context.arc(p.projX, p.projY, m * particleRad, 0, 2 * Math.PI, false);
				context.closePath();
				context.fill();
			}
			p = nextParticle;
		}
	}
    setInterval(onTimer, 1000 / 60);
}