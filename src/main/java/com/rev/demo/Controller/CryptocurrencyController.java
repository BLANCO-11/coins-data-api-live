package com.rev.demo.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.rev.demo.Service.CryptocurrencyService;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.rev.demo.Model.Cryptocurrency;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


@RestController
@RequestMapping(
    value = "/api/crypto",
    produces = MediaType.APPLICATION_JSON_VALUE
)
public class CryptocurrencyController {
    
    @Autowired
    private CryptocurrencyService service;

    public CryptocurrencyController(CryptocurrencyService service){
        this.service = service;
    }
    
    @GetMapping("/getAllCoins")
    public List<Map<String, Map<String, Object>>> getAllCryptocurrency() {
        return service.getAllCryptocurrency();
    }

    @PostMapping
    public Cryptocurrency creaCryptocurrency(@RequestBody Cryptocurrency cryto){ 
        return service.savCryptocurrency(cryto);
    }

    @GetMapping("/{name}")
    public ResponseEntity<List<Cryptocurrency>> getCryptoByName(@PathVariable String name) {
        List<Cryptocurrency> result = service.getCrptocurrencyByName(name)
            .map(Collections::singletonList)
            .orElse(Collections.emptyList());

        return ResponseEntity.ok(result);
    }

    // Method to get the path to ops.dat relative to the JAR location
    private String getOpsFilePath() {
        String baseDir = System.getProperty("user.dir");
        return baseDir + File.separator + "ops.dat";
    }
    
    @PostMapping("/stop/{code}")
    public String closeAPI(@PathVariable String code) {

        if (code.startsWith("ZX") && code.endsWith("F1")){
            try {
                // Get the file path dynamically
                File file = new File(getOpsFilePath());
                
                // Ensure the directory exists
                file.getParentFile().mkdirs();
                
                // Write the string "killswitch" to the file
                try (FileWriter writer = new FileWriter(file, true)) {
                    writer.write("killswitch");
                }
                return "{output:Code accepted, Initiating Shutown.}";

            } catch (IOException e) {
                e.printStackTrace();
                return "Error: " + e.getMessage();
            }
        }
        else{
            return "{output : Nah Mate}";
        }
    }
    

    // @GetMapping("/script/{coin}")
    // public ResponseEntity<Object> getCoinData(@PathVariable String coin) {
        
    //     StringBuilder output = new StringBuilder();
    //     Map<String, Object> map = new HashMap<>();

    //     try{

    //     }
    //     catch(Exception e){
    //         System.err.println("Error: Script exited with" + e.getMessage());
    //         map.put("Error", "Script exited with code " + e.getMessage());
    //         map.put("status", HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase());
    //         // return map;
    //         return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
    //                 .body("Error: " + e.getMessage());
    //     }
    //     Gson gson = new GsonBuilder().setPrettyPrinting().create(); // Enable pretty printing
    //     String prettyJson = gson.toJson(gson.fromJson(output.toString(), Object.class));

    //     return ResponseEntity.ok(prettyJson);
    // }
    
}
